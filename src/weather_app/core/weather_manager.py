from typing import Optional
from weather_app.infra.geo_service import GeoService
from weather_app.infra.weather_service import WeatherService
from weather_app.models.weather import WeatherData

class WeatherManager:
    """Manager to coordinate weather and location services."""

    def __init__(self, geo_service: GeoService, weather_service: WeatherService):
        self.geo_service = geo_service
        self.weather_service = weather_service

    def fetch_weather_for_city(self, city: str) -> Optional[WeatherData]:
        """Fetch weather data for a given city name.

        Args:
            city: City name.

        Returns:
            WeatherData if all steps succeed, else None.
        """
        location = self.geo_service.get_location(city)
        if not location:
            return None

        timezone = self.geo_service.get_timezone(location.latitude, location.longitude)
        if not timezone:
            return None

        return self.weather_service.get_weather(city, timezone)
