from core.api.api_permission import APIPermission
from core.adapters.news_adapter import NewsAdapter


def test_news_adapter_success():
    permission = APIPermission({"news"})
    adapter = NewsAdapter(permission)

    response = adapter.get_news("technology")

    assert response.title == "News"
    assert response.payload["topic"] == "technology"
    assert isinstance(response.payload["headlines"], list)
    assert len(response.payload["headlines"]) <= 5


def test_news_adapter_requires_permission():
    permission = APIPermission(set())
    adapter = NewsAdapter(permission)

    try:
        adapter.get_news("economy")
        assert False, "Permission should have been denied"
    except Exception:
        assert True


def test_news_adapter_rejects_empty_topic():
    permission = APIPermission({"news"})
    adapter = NewsAdapter(permission)

    try:
        adapter.get_news("")
        assert False, "Empty topic should fail"
    except ValueError:
        assert True
