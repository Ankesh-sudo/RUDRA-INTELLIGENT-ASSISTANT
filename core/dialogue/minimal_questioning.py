# core/dialogue/minimal_questioning.py

from typing import Optional


class MinimalQuestioning:
    """
    Day 74 — Minimal questioning policy.

    Ask a follow-up ONLY if:
    - intent is ambiguous
    - required slots are missing
    """

    AMBIGUOUS_INTENTS = {"UNKNOWN"}

    def should_ask(self, intent: Optional[str], missing_slots: bool) -> bool:
        if intent in self.AMBIGUOUS_INTENTS:
            return True
        if missing_slots:
            return True
        return False
