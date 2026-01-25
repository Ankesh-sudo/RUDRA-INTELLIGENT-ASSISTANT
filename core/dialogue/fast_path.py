# core/dialogue/fast_path.py

from typing import Optional


class FastPath:
    """
    Day 75 — Fast-path resolution helpers.

    Rules:
    - Deterministic
    - Read-only
    - No mutation
    """

    def can_skip_intent_resolution(
        self,
        cached_intent: Optional[str],
        current_text: str,
    ) -> bool:
        if not cached_intent:
            return False
        if not current_text:
            return False
        # identical short utterances can reuse intent
        return len(current_text.strip()) <= 3
