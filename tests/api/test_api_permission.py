import pytest
from core.api.api_permission import APIPermission
from core.api.api_errors import APIPermissionDenied


def test_permission_allowed():
    p = APIPermission({"weather"})
    p.check("weather")


def test_permission_denied():
    p = APIPermission({"weather"})
    with pytest.raises(APIPermissionDenied):
        p.check("news")
