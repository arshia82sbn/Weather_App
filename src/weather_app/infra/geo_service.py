from typing import Optional
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from weather_app.models.location import LocationData

class GeoService:
    """Service for geographical information and timezones."""

    def __init__(self, user_agent: str = "weather_app"):
        self.geolocator = Nominatim(user_agent=user_agent)
        self.tf = TimezoneFinder()

    def get_location(self, city: str) -> Optional[LocationData]:
        """Get geographical coordinates for a city.

        Args:
            city: Name of the city.

        Returns:
            LocationData if found, else None.
        """
        try:
            location = self.geolocator.geocode(city)
            if location:
                return LocationData(
                    name=city,
                    latitude=location.latitude,
                    longitude=location.longitude
                )
            return None
        except Exception:
            return None

    def get_timezone(self, latitude: float, longitude: float) -> Optional[pytz.BaseTzInfo]:
        """Get timezone for given coordinates.

        Args:
            latitude: Latitude.
            longitude: Longitude.

        Returns:
            pytz timezone object if found, else None.
        """
        try:
            timezone_str = self.tf.timezone_at(lng=longitude, lat=latitude)
            if timezone_str:
                return pytz.timezone(timezone_str)
            return None
        except Exception:
            return None
