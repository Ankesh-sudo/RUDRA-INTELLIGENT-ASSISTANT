import pytest
from core.api.api_contract import APIContract


def test_valid_contract():
    c = APIContract("weather", "/x", "GET", {"city": str})
    c.validate()


def test_invalid_method():
    with pytest.raises(ValueError):
        APIContract("x", "/x", "POST", {}).validate()
