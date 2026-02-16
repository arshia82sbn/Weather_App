from unittest.mock import MagicMock
from datetime import datetime
import pytz
from weather_app.core.weather_manager import WeatherManager
from weather_app.models.weather import WeatherData
from weather_app.models.location import LocationData

def test_fetch_weather_for_city_success():
    # Setup
    geo_service = MagicMock()
    weather_service = MagicMock()

    mock_location = LocationData(name="London", latitude=51.5, longitude=-0.12)
    mock_timezone = pytz.timezone("Europe/London")
    mock_weather = WeatherData(
        temp=20.0, condition="Clear", description="sunny",
        pressure=1013, humidity=50, wind_speed=5.0,
        local_time=datetime.now(mock_timezone), city="London"
    )

    geo_service.get_location.return_value = mock_location
    geo_service.get_timezone.return_value = mock_timezone
    weather_service.get_weather.return_value = mock_weather

    manager = WeatherManager(geo_service, weather_service)

    # Execute
    result = manager.fetch_weather_for_city("London")

    # Assert
    assert result == mock_weather
    geo_service.get_location.assert_called_with("London")
    geo_service.get_timezone.assert_called_with(51.5, -0.12)
    weather_service.get_weather.assert_called_with("London", mock_timezone)

def test_fetch_weather_for_city_location_not_found():
    # Setup
    geo_service = MagicMock()
    weather_service = MagicMock()
    geo_service.get_location.return_value = None

    manager = WeatherManager(geo_service, weather_service)

    # Execute
    result = manager.fetch_weather_for_city("Unknown")

    # Assert
    assert result is None
    weather_service.get_weather.assert_not_called()
