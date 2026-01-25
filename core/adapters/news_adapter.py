from typing import List
from core.api.api_registry import APIRegistry
from core.api.api_permission import APIPermission
from core.api.api_client import APIClient
from .adapter_response import AdapterResponse


class NewsAdapter:
    """
    Read-only News adapter.
    Headlines only. No analysis, no opinion.
    """

    MAX_HEADLINES = 5
    MAX_LENGTH = 120

    def __init__(self, permission: APIPermission):
        self.permission = permission
        self.client = APIClient()

    def get_news(self, topic: str) -> AdapterResponse:
        if not topic or not topic.strip():
            raise ValueError("Topic is required")

        # Permission gate
        self.permission.check("news")

        contract = APIRegistry.get("news")
        self.client.fetch(contract, {"topic": topic})

        # Deterministic, neutral, stubbed headlines
        headlines: List[str] = [
            f"{topic.title()} update reported by official sources",
            f"Latest developments related to {topic}",
            f"{topic.title()} reported in recent public briefing",
            f"New information released regarding {topic}",
            f"{topic.title()} remains under observation",
        ]

        # Enforce limits
        cleaned = []
        for h in headlines[: self.MAX_HEADLINES]:
            text = h.strip()
            if len(text) > self.MAX_LENGTH:
                text = text[: self.MAX_LENGTH]
            cleaned.append(text)

        return AdapterResponse.build(
            title="News",
            payload={"topic": topic, "headlines": cleaned},
            source="news",
        )
