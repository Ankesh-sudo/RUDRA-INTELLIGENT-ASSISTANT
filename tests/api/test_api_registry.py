import pytest
from core.api.api_registry import APIRegistry
from core.api.api_errors import APIRegistryError


def test_registry_fetch():
    api = APIRegistry.get("weather")
    assert api.name == "weather"


def test_registry_missing():
    with pytest.raises(APIRegistryError):
        APIRegistry.get("unknown")
