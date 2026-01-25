from core.api.api_registry import APIRegistry
from core.api.api_permission import APIPermission
from core.api.api_client import APIClient
from .adapter_response import AdapterResponse


class WeatherAdapter:
    """
    Weather data adapter (stubbed).
    """

    def __init__(self, permission: APIPermission):
        self.permission = permission
        self.client = APIClient()

    def get_weather(self, city: str) -> AdapterResponse:
        if not city or not city.strip():
            raise ValueError("City is required")

        # Permission gate
        self.permission.check("weather")

        contract = APIRegistry.get("weather")
        response = self.client.fetch(contract, {"city": city})

        # Deterministic stubbed interpretation
        payload = {
            "city": city,
            "temperature_c": 25,
            "condition": "Clear",
        }

        return AdapterResponse.build(
            title="Weather",
            payload=payload,
            source=response.source,
        )
