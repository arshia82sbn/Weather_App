from unittest.mock import patch, MagicMock
import pytest
import pytz
from weather_app.infra.weather_service import OpenWeatherMapService

@patch('requests.get')
def test_openweathermap_service_success(mock_get):
    # Setup
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "cod": 200,
        "weather": [{"main": "Clouds", "description": "broken clouds"}],
        "main": {"temp": 293.15, "pressure": 1012, "humidity": 72},
        "wind": {"speed": 4.12}
    }
    mock_get.return_value = mock_response

    service = OpenWeatherMapService(api_key="test_key")
    timezone = pytz.timezone("UTC")

    # Execute
    result = service.get_weather("London", timezone)

    # Assert
    assert result is not None
    assert result.temp == 20.0
    assert result.condition == "Clouds"
    assert result.city == "London"

@patch('requests.get')
def test_openweathermap_service_failure(mock_get):
    # Setup
    mock_response = MagicMock()
    mock_response.json.return_value = {"cod": 404, "message": "city not found"}
    mock_get.return_value = mock_response

    service = OpenWeatherMapService(api_key="test_key")
    timezone = pytz.timezone("UTC")

    # Execute
    result = service.get_weather("Unknown", timezone)

    # Assert
    assert result is None
