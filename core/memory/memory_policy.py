"""
Memory Decision Engine (Gatekeeper)

Responsibilities:
- Decide WHETHER a memory should be written
- Decide WHERE it should go (STM / LTM / NONE)
- Enforce confidence thresholds
- Prevent memory pollution
"""

from enum import Enum


class MemoryType(Enum):
    NONE = "none"
    STM = "short_term"
    LTM = "long_term"


class MemoryDecisionEngine:
    """
    All memory writes MUST pass through this engine.
    No bypasses. Ever.
    """

    # ===============================
    # DAY 21.2 — TIGHTENED THRESHOLDS
    # ===============================

    # Raised confidence threshold
    MIN_CONFIDENCE = 0.70

    # STM intent whitelist (explicit)
    STM_INTENT_WHITELIST = {
        "open_browser",
        "search",
        "set_reminder",
        "play_music",
        "note",
    }

    # Intents that must NEVER be stored
    INTENT_BLACKLIST = {
        "greeting",
        "help",
        "exit",
        "unknown",
    }

    @staticmethod
    def decide(
        *,
        intent_name: str | None,
        confidence: float,
        content_type: str,
        is_repeated: bool = False
    ) -> MemoryType:
        """
        Parameters:
        - intent_name: resolved intent (string)
        - confidence: final confidence score
        - content_type: semantic category of content
          Allowed values (LOCKED):
            - "command"
            - "conversation"
            - "user_fact"
            - "user_preference"
            - "system"
        - is_repeated: whether the info was seen multiple times (future use)

        Returns:
        - MemoryType.NONE / STM / LTM
        """

        # -------------------------------------------------
        # 1) Confidence gate (STRICT)
        # -------------------------------------------------
        if confidence < MemoryDecisionEngine.MIN_CONFIDENCE:
            return MemoryType.NONE

        # -------------------------------------------------
        # 2) Never store system-level or raw commands
        # -------------------------------------------------
        if content_type in {"command", "system"}:
            return MemoryType.NONE

        # -------------------------------------------------
        # 3) Intent must be valid and allowed
        # -------------------------------------------------
        if not intent_name:
            return MemoryType.NONE

        if intent_name in MemoryDecisionEngine.INTENT_BLACKLIST:
            return MemoryType.NONE

        # -------------------------------------------------
        # 4) STM admission (conversation only, whitelisted)
        # -------------------------------------------------
        if content_type == "conversation":
            if intent_name in MemoryDecisionEngine.STM_INTENT_WHITELIST:
                return MemoryType.STM
            return MemoryType.NONE

        # -------------------------------------------------
        # 5) LTM is LOCKED for Day 21.x
        # -------------------------------------------------
        # Even stable user data is intentionally blocked here.
        if content_type in {"user_fact", "user_preference"}:
            return MemoryType.NONE

        # -------------------------------------------------
        # Default: do not store
        # -------------------------------------------------
        return MemoryType.NONE
