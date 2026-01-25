from core.api.api_permission import APIPermission
from core.adapters.time_adapter import TimeAdapter


def test_time_adapter_success():
    permission = APIPermission({"weather"})
    adapter = TimeAdapter(permission)

    result = adapter.get_time("Delhi")
    assert result.title == "Time"
    assert "utc_time" in result.payload
