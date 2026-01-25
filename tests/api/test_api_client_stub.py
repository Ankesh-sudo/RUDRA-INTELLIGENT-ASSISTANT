from core.api.api_client import APIClient
from core.api.api_registry import APIRegistry


def test_stubbed_client():
    api = APIRegistry.get("weather")
    client = APIClient()

    response = client.fetch(api, {"city": "Delhi"})
    assert response.data["params"]["city"] == "Delhi"
