from core.api.api_permission import APIPermission
from core.adapters.weather_adapter import WeatherAdapter


def test_weather_adapter_success():
    permission = APIPermission({"weather"})
    adapter = WeatherAdapter(permission)

    result = adapter.get_weather("Delhi")
    assert result.title == "Weather"
    assert result.payload["city"] == "Delhi"
