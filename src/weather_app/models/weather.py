from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class WeatherData:
    """Data class for weather information."""
    temp: float
    condition: str
    description: str
    pressure: int
    humidity: int
    wind_speed: float
    local_time: datetime
    city: str
