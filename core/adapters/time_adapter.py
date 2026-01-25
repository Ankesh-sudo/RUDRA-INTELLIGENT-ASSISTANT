from datetime import datetime, timezone
from core.api.api_registry import APIRegistry
from core.api.api_permission import APIPermission
from core.api.api_client import APIClient
from .adapter_response import AdapterResponse


class TimeAdapter:
    """
    Time data adapter (UTC-based stub).
    """

    def __init__(self, permission: APIPermission):
        self.permission = permission
        self.client = APIClient()

    def get_time(self, city: str) -> AdapterResponse:
        if not city or not city.strip():
            raise ValueError("City is required")

        # Permission gate (reuse weather-style permission model)
        self.permission.check("weather")

        contract = APIRegistry.get("weather")
        response = self.client.fetch(contract, {"city": city})

        now_utc = datetime.now(timezone.utc)

        payload = {
            "city": city,
            "utc_time": now_utc.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return AdapterResponse.build(
            title="Time",
            payload=payload,
            source=response.source,
        )
