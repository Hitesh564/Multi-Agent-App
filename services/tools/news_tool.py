
import re
import requests
from datetime import datetime, timedelta
from config import settings
from services.llm_service import LLMService
from utils.logger import get_logger

logger = get_logger(__name__)

# 🧠 Normalize and clean topic text
def clean_topic_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\?\!\.,;:\"]', ' ', text)
    text = re.sub(r'\b(any|please|show|tell|me|give|provide|find|find me|recent|recently|latest|about|in|on|for|news|updates|update|headlines|article|articles|today|yesterday|currently|currently|new|sector|industry)\b', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 🧠 Extract topic, category, country from query
def extract_topic(query: str) -> dict:
    query_lower = query.lower().strip()
    normalized = re.sub(r'[\?\!\.,;:\"]', ' ', query_lower)
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    # Categories
    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    category = None
    for cat in categories:
        if re.search(r'\b' + re.escape(cat) + r'\b', normalized):
            category = cat
            normalized = re.sub(r'\b' + re.escape(cat) + r'\b', ' ', normalized)
            break

    # Countries
    countries = {
        "us": "us", "usa": "us", "america": "us",
        "india": "in", "indian": "in",
        "uk": "gb", "britain": "gb", "england": "gb",
        "china": "cn", "global": None, "world": None
    }
    country = None
    for key, code in countries.items():
        if re.search(r'\b' + re.escape(key) + r'\b', normalized):
            country = code
            normalized = re.sub(r'\b' + re.escape(key) + r'\b', ' ', normalized)
            break

    # Try explicit topic patterns first
    patterns = [
        r'^(?:what(?:\'s| is)? )?(?:the )?(?:most )?(?:recent|latest) news (?:about|on|in|for) (?P<topic>.+)$',
        r'^(?:any|some|other|latest|recent) (?:news|updates|headlines) (?:about|on|in|for) (?P<topic>.+)$',
        r'news (?:about|on|in|from|for) (?P<topic>.+)',
        r'^(?P<topic>.+?)\s+(?:news|updates|headlines)$'
    ]

    topic = None
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if match:
            topic = match.group('topic').strip()
            break

    if not topic:
        stripped = normalized
        stripped = re.sub(r'\b(any|please|show|tell|me|give|provide|find|find me|recent|recently|latest|about|in|on|for|from|to|into|at|by|with|news|updates|update|headlines|article|articles|today|yesterday|currently|new|please|other)\b', ' ', stripped)
        stripped = re.sub(r'\s+', ' ', stripped).strip()
        topic = stripped

    topic = re.sub(r'\s+', ' ', topic).strip()

    if not topic and category:
        topic = category
    if not topic and country:
        topic = f"news from {country.upper()}"
    if not topic:
        topic = "general"

    return {
        "topic": topic,
        "category": category,
        "country": country
    }

# 🧠 Fetch news from NewsAPI
def fetch_news(topic: str, category: str = None, country: str = None) -> dict | None:
    api_key = settings.NEWS_API_KEY
    if not api_key or api_key == "your_news_api_key":
        logger.warning("No valid NewsAPI key found.")
        return None

    if category or country:
        url = "https://newsapi.org/v2/top-headlines"
    else:
        url = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "pageSize": 7,
        "apiKey": api_key,
        "language": "en"
    }

    if category:
        params["category"] = category
    if country:
        params["country"] = country

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            logger.error(f"NewsAPI error: {data.get('message')}")
            return None

        articles = data.get("articles", [])
        if not articles:
            return {"articles": []}

        # Filter and format articles
        formatted_articles = []
        for article in articles[:7]:  # Limit to 7
            published_at = article.get("publishedAt")
            if published_at:
                try:
                    dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    time_ago = get_time_ago(dt)
                except:
                    time_ago = "Unknown"
            else:
                time_ago = "Unknown"

            formatted_articles.append({
                "title": article.get("title", "No title"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "time": time_ago,
                "description": article.get("description", "No description available."),
                "url": article.get("url", "")
            })

        return {"articles": formatted_articles}

    except requests.RequestException as e:
        logger.error(f"NewsAPI request failed: {str(e)}")
        return None

# 🧠 Get time ago string
def get_time_ago(dt: datetime) -> str:
    now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    diff = now - dt

    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds // 3600 > 0:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds // 60 > 0:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "Just now"

# 🧠 Format news output
def format_news_output(data: dict, topic: str) -> str:
    articles = data.get("articles", [])
    if not articles:
        return f"No recent news found for {topic}."

    # Remove markdown clutter and emojis from title
    output = "Latest Updates:\n\n"

    for article in articles[:5]:  # Limit to 5 max
        title = article['title'].replace('*', '').strip()
        desc = article.get('description', '') or ''
        desc = desc.replace('\n', ' ').strip()
        
        # Limit description to 2-3 lines worth (approx 150 chars)
        if len(desc) > 150:
            desc = desc[:147] + "..."
            
        time_str = article['time']
        url = article['url']
        
        output += f"- {title}\n"
        if desc:
            output += f"  {desc}\n"
        output += f"  Date: {time_str}\n"
        output += f"  Link: {url}\n\n"

    return output.strip()

# 🧠 Generate LLM summary
def generate_llm_summary(articles: list, topic: str) -> str:
    if not articles:
        return ""

    try:
        llm = LLMService()
        headlines = "\n".join([f"- {art['title']}" for art in articles[:5]])  # Top 5 for summary

        prompt = f"""
Based on these recent news headlines about {topic}, provide a 3-4 line summary of the current trends or key developments.
Do not hallucinate or add information not implied by the headlines.

Headlines:
{headlines}

Summary:
"""

        summary = llm.generate_response(prompt, system_prompt="You are a news summarizer. Keep it factual and concise. Do not use asterisks or bold markdown.")
        if summary and not summary.startswith("Error"):
            cleaned_summary = summary.replace('*', '').strip()
            return f"\nSummary:\n{cleaned_summary}"
        else:
            return ""

    except Exception as e:
        logger.error(f"LLM summary failed: {str(e)}")
        return ""

# 🛠️ Main news tool
def news_tool(query: str) -> str:
    logger.info(f"News tool received query: {query}")

    extracted = extract_topic(query)
    topic = extracted["topic"]
    category = extracted["category"]
    country = extracted["country"]

    if not topic or topic == "general":
        if category:
            topic = category
        elif country:
            topic = f"news from {country.upper() if country else 'global'}"
        else:
            return "Please specify a topic for news, e.g. 'latest news about AI'."

    logger.info(f"Extracted topic: {topic}, category: {category}, country: {country}")

    data = fetch_news(topic, category, country)
    if not data:
        return f"⚠️ Unable to fetch news for '{topic}'. Please check your NEWS_API_KEY or try again later."

    output = format_news_output(data, topic)

    # Optional LLM summary
    summary = generate_llm_summary(data.get("articles", []), topic)
    if summary:
        output += summary

    return output