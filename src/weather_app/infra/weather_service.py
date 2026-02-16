from abc import ABC, abstractmethod
from typing import Optional
import requests
from datetime import datetime
import pytz
from weather_app.models.weather import WeatherData

class WeatherService(ABC):
    """Abstract base class for weather services."""

    @abstractmethod
    def get_weather(self, city: str, timezone: pytz.BaseTzInfo) -> Optional[WeatherData]:
        """Fetch weather data for a city."""
        pass

class OpenWeatherMapService(WeatherService):
    """Implementation of WeatherService using OpenWeatherMap API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str, timezone: pytz.BaseTzInfo) -> Optional[WeatherData]:
        """Fetch weather data from OpenWeatherMap.

        Args:
            city: City name.
            timezone: Timezone for local time calculation.

        Returns:
            WeatherData if successful, else None.
        """
        url = f"{self.base_url}?q={city}&appid={self.api_key}"
        try:
            response = requests.get(url)
            json_data = response.json()
            if json_data.get("cod") != 200:
                return None

            condition = json_data['weather'][0]['main']
            description = json_data['weather'][0]['description']
            temp = round(json_data['main']['temp'] - 273.15, 1)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            local_time = datetime.now(timezone)

            return WeatherData(
                temp=temp,
                condition=condition,
                description=description,
                pressure=pressure,
                humidity=humidity,
                wind_speed=wind,
                local_time=local_time,
                city=city
            )
        except Exception:
            return None
