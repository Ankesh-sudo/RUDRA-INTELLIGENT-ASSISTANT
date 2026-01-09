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

    # Tunable thresholds (locked for now)
    MIN_CONFIDENCE = 0.60

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

        # 1) Confidence gate
        if confidence < MemoryDecisionEngine.MIN_CONFIDENCE:
            return MemoryType.NONE

        # 2) Never store system or commands
        if content_type in {"command", "system"}:
            return MemoryType.NONE

        # 3) Conversational continuity → STM
        if content_type == "conversation":
            return MemoryType.STM

        # 4) Stable user data → LTM
        if content_type in {"user_fact", "user_preference"}:
            return MemoryType.LTM

        # Default: do not store
        return MemoryType.NONE
