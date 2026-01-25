from core.adapters.adapter_response import AdapterResponse


def test_adapter_response_build():
    r = AdapterResponse.build(
        title="Weather",
        payload={"x": 1},
        source="weather",
    )
    assert r.title == "Weather"
    assert "timestamp" in r.__dict__
