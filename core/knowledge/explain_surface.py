from typing import Optional, Dict
from core.knowledge.engine import KnowledgeEngine
from core.knowledge.explain_policy import MISS_MESSAGE


class KnowledgeExplainSurface:
    """
    Day 79 — Explainable knowledge responses.

    Returns a uniform envelope:
    - On hit: answer + citation + topic
    - On miss: explicit, safe message
    """

    def __init__(self, engine: KnowledgeEngine):
        self._engine = engine

    def respond(self, query: str) -> Dict[str, str]:
        result: Optional[dict] = self._engine.answer(query)

        if not result:
            return {
                "answer": MISS_MESSAGE,
                "citation": "",
                "topic": "unknown",
            }

        return {
            "answer": result["answer"],
            "citation": result["citation"],
            "topic": result["topic"],
        }
