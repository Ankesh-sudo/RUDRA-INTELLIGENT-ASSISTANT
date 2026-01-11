# core/memory/classifier.py

import re
from typing import Optional


class MemoryClassifier:
    PREFERENCE_KEYWORDS = [
        "like", "love", "prefer", "enjoy",
        "dislike", "hate", "don't like", "do not like"
    ]

    HABIT_KEYWORDS = [
        "usually", "every day", "daily", "often", "always",
        "at night", "in the morning",
        "i wake up", "i sleep", "i study", "i work"
    ]

    def classify(self, text: str) -> Optional[str]:
        """
        Deterministically classify memory text.

        Returns:
            "fact", "preference", "habit"
            None if ambiguous
        """
        normalized = text.lower()

        is_preference = any(k in normalized for k in self.PREFERENCE_KEYWORDS)
        is_habit = any(k in normalized for k in self.HABIT_KEYWORDS)

        if is_preference and is_habit:
            return None

        if is_preference:
            return "preference"

        if is_habit:
            return "habit"

        return "fact"
