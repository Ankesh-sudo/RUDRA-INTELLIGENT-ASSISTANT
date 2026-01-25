import pytest
from core.api.api_response import APIResponse
from core.api.api_errors import APIInvalidResponse


def test_response_build():
    r = APIResponse.build({"x": 1}, "test")
    assert r.source == "test"


def test_response_invalid():
    with pytest.raises(APIInvalidResponse):
        APIResponse.build(None, "x")
