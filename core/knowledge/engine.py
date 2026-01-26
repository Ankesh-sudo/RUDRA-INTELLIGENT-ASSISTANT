from typing import List, Optional
from core.knowledge.schema import DharmaRow


class KnowledgeEngine:
    """
    Day 76 — CSV-only, zero-hallucination knowledge engine.

    Rules:
    - NO generation
    - NO guessing
    - NO inference beyond stored rows
    """

    def __init__(self, rows: List[DharmaRow]):
        self._rows = rows

    # -------------------------------------------------
    # EXACT QUESTION MATCH (STRICT)
    # -------------------------------------------------
    def answer(self, query: str) -> Optional[dict]:
        """
        Exact question lookup.
        Returns a single answer only if the question matches exactly.
        """
        q = query.lower().strip()

        for r in self._rows:
            if q == r.question.lower():
                return {
                    "answer": r.answer,
                    "citation": r.citation,
                    "topic": r.topic,
                }

        return None  # explicit miss (no guessing)

    # -------------------------------------------------
    # TOPIC QUERY (SAFE AGGREGATION)
    # -------------------------------------------------
    def query(self, topic: str) -> Optional[str]:
        """
        Topic-level lookup.
        Aggregates known answers for a topic.
        No inference, no generation.
        """
        t = topic.lower().strip()

        matches = [r for r in self._rows if r.topic.lower() == t]

        if not matches:
            return None

        # Deterministic aggregation
        parts = []
        for r in matches:
            parts.append(f"- {r.answer}")

            if r.citation:
                parts.append(f"  ({r.citation})")

        return "\n".join(parts)
