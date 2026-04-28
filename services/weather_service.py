import requests
from utils.logger import get_logger

logger = get_logger(__name__)

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_coordinates(self, city: str):
        """
        Convert city name → latitude & longitude
        """
        try:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
            response = requests.get(geo_url)

            if response.status_code != 200:
                logger.error(f"Geocoding API error: {response.text}")
                return None

            data = response.json()

            if not data:
                logger.warning(f"No location found for city: {city}")
                return None

            lat = data[0]["lat"]
            lon = data[0]["lon"]

            return lat, lon

        except Exception as e:
            logger.error(f"Geocoding failed: {str(e)}")
            return None

    def get_weather(self, city: str):
        """
        Get weather using lat/lon (robust method)
        """
        try:
            coords = self.get_coordinates(city)

            if not coords:
                return f"❌ Couldn't find location for '{city}'. Try another city."

            lat, lon = coords

            weather_url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            )

            response = requests.get(weather_url)

            if response.status_code != 200:
                logger.error(f"Weather API error: {response.text}")
                return "❌ Weather service error. Try again later."

            data = response.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]

            return (
                f"🌤 Weather in {city.title()}:\n"
                f"Temperature: {temp}°C\n"
                f"Condition: {condition}\n"
                f"Humidity: {humidity}%"
            )

        except Exception as e:
            logger.error(f"Weather fetch failed: {str(e)}")
            return "❌ Weather service is currently unavailable."