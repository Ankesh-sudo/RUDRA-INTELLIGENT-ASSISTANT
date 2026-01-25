from typing import List, Optional
from core.knowledge.schema import DharmaRow


class KnowledgeEngine:
    """
    Day 76 — CSV-only, zero-hallucination knowledge engine.
    """

    def __init__(self, rows: List[DharmaRow]):
        self._rows = rows

    def answer(self, query: str) -> Optional[dict]:
        q = query.lower().strip()

        for r in self._rows:
            if q == r.question.lower():
                return {
                    "answer": r.answer,
                    "citation": r.citation,
                    "topic": r.topic,
                }

        return None  # explicit miss (no guessing)
