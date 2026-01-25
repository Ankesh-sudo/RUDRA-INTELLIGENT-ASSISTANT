# core/dialogue/context_policy.py

from typing import Optional
from core.dialogue.session_dialogue_state import SessionDialogueState


class ContextPolicy:
    """
    Day 74 — Adaptive context policy.

    - Shortens TTL for trivial intents
    - Preserves TTL for multi-turn topics
    - Enforces aggressive pruning
    """

    SHORT_TTL = 20.0
    DEFAULT_TTL = 120.0
    LONG_TTL = 300.0

    def apply(self, state: SessionDialogueState, intent: Optional[str]) -> None:
        if intent in {"ACKNOWLEDGEMENT", "SMALL_TALK"}:
            state.ttl_sec = self.SHORT_TTL
        elif intent in {"CLARIFICATION"}:
            state.ttl_sec = self.LONG_TTL
        else:
            state.ttl_sec = self.DEFAULT_TTL
