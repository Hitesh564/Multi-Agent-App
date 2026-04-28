import re
from config import settings
from services.weather_service import WeatherService
from utils.logger import get_logger

logger = get_logger(__name__)


# 🧠 Better city extraction
def extract_city(query: str):
    query_lower = query.lower().strip()

    # 🔹 Remove noise words added by LLM
    noise_words = ["conditions", "condition", "weather", "temperature", "humidity", "for"]
    for word in noise_words:
        query_lower = query_lower.replace(word, "")

    # 🔹 Pattern 1: "in <city>"
    match = re.search(r'in ([a-zA-Z\s,]+)', query_lower)
    if match:
        return match.group(1).strip()

    # 🔹 Pattern 2: "of <city>"
    match = re.search(r'of ([a-zA-Z\s,]+)', query_lower)
    if match:
        return match.group(1).strip()

    # 🔹 Pattern 3: fallback → last words (for queries like "weather delhi")
    words = query_lower.split()
    if len(words) >= 1:
        # assume last 1–2 words are city
        return " ".join(words[-2:]).strip()

    return None


# 🧠 Clean extracted city
def clean_city(city: str):
    city = city.strip()

    # Remove extra words
    city = re.sub(r'[^a-zA-Z\s,]', '', city)

    # Normalize casing
    city = city.title()

    return city


# 🛠️ Main weather tool
def weather_tool(query: str) -> str:
    logger.info(f"Weather tool received query: {query}")

    city = extract_city(query)

    if not city:
        return "Please specify a city, e.g. 'weather in Delhi'."

    city = clean_city(city)

    logger.info(f"Extracted city: {city}")

    api_key = settings.OPENWEATHER_API_KEY

    # 🔥 Check API key
    if not api_key or api_key == "your_openweather_key":
        logger.warning("No valid OpenWeather API key found.")
        return (
            f"🌤 Weather in {city}:\n"
            f"- Condition: Sunny\n"
            f"- Temperature: 28°C\n"
            f"- Humidity: 60%\n\n"
            f"*(Mock data — API key not configured)*"
        )

    try:
        weather_service = WeatherService(api_key)
        result = weather_service.get_weather(city)

        # 🔥 Handle bad responses
        if not result or "couldn't find" in result.lower():
            return f"❌ Couldn't find weather for '{city}'. Try a nearby major city."

        return result

    except Exception as e:
        logger.error(f"Weather tool failed: {str(e)}")
        return "⚠️ Weather service is currently unavailable. Please try again."