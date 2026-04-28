import re
import yfinance as yf
from utils.logger import get_logger

logger = get_logger(__name__)


# 🧠 Extract company/ticker from query
def extract_company(query: str) -> str:
    query = query.lower()

    # remove noise words
    query = re.sub(r"(stock|price|of|the|tell|me|give|current|for|company)", "", query)

    return query.strip()


# 🧠 Resolve ticker (robust + simple)
def resolve_ticker(query: str):
    raw_query = query.strip()
    company = extract_company(query)

    # 🔥 Step 1: Direct ticker detection (IMPORTANT)
    words = raw_query.split()
    for w in words:
        if "." in w or (w.isupper() and len(w) <= 12):
            return w.upper()

    # 🔥 Step 2: Known companies (IMPORTANT for India)
    COMMON_MAP = {
        "axis bank": "AXISBANK.NS",
        "airtel": "BHARTIARTL.NS",
        "reliance": "RELIANCE.NS",
        "tcs": "TCS.NS",
        "infosys": "INFY.NS",
        "hdfc bank": "HDFCBANK.NS",
        "icici": "ICICIBANK.NS",
        "netflix": "NFLX",
        "apple": "AAPL",
        "tesla": "TSLA",
        "amazon": "AMZN",
        "google": "GOOGL",
        "microsoft": "MSFT"
    }

    for name, symbol in COMMON_MAP.items():
        if name in company:
            return symbol

    # 🔥 Step 3: Fallback (best guess)
    return company.replace(" ", "").upper()


# 🧠 Fetch stock data (RELIABLE METHOD)
def get_stock_price(ticker_symbol: str):
    try:
        ticker = yf.Ticker(ticker_symbol)

        # 🔥 Use history (most reliable)
        hist = ticker.history(period="1d")

        if hist is not None and not hist.empty:
            price = hist["Close"].iloc[-1]

            return {
                "name": ticker_symbol,
                "symbol": ticker_symbol,
                "price": round(price, 2)
            }

    except Exception as e:
        logger.error(f"Stock fetch failed: {e}")

    return None


# 🧠 Format output
def format_stock_output(data: dict) -> str:
    return f"""
📈 **Stock: {data['symbol']}**

💰 Current Price: {data['price']}
"""


# 🛠️ MAIN TOOL FUNCTION
def stock_tool(query: str) -> str:
    logger.info(f"Stock tool received query: {query}")

    ticker = resolve_ticker(query)

    if not ticker:
        return "❌ Couldn't identify the stock. Try using a company name or ticker (e.g., Apple, AAPL, Reliance)."

    data = get_stock_price(ticker)

    if not data:
        return f"⚠️ Live stock data unavailable for {ticker}. Please try again."

    return format_stock_output(data)