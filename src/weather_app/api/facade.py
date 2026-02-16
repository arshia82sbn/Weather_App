from typing import Optional
from weather_app.core.weather_manager import WeatherManager
from weather_app.models.weather import WeatherData
from weather_app.infra.geo_service import GeoService
from weather_app.infra.weather_service import OpenWeatherMapService

class WeatherFacade:
    """Facade for the Weather Application."""

    def __init__(self, api_key: str):
        geo_service = GeoService()
        weather_service = OpenWeatherMapService(api_key)
        self.manager = WeatherManager(geo_service, weather_service)

    def get_weather_info(self, city: str) -> Optional[WeatherData]:
        """Retrieve weather information for a city.

        Args:
            city: The city name.

        Returns:
            WeatherData if successful, else None.
        """
        return self.manager.fetch_weather_for_city(city)
