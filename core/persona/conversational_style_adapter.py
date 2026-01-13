# core/persona/conversational_style_adapter.py

from typing import Dict


class ConversationalStyleAdapter:
    """
    Applies cosmetic, suffix-only conversational style.
    This adapter is meaning-preserving and non-authoritative.
    """

    def __init__(self) -> None:
        pass

    def apply(
        self,
        text: str,
        *,
        persona_enabled: bool,
        explain_trace: Dict,
    ) -> str:
        """
        Entry point for conversational styling.

        Day 32.1 behavior:
        - No-op
        - Returns text unchanged
        - Emits explain trace stub
        """

        explain_trace["persona.style_applied"] = False
        explain_trace["persona.style_mode"] = "conversational_hindi"
        explain_trace["persona.style_reason"] = "not_implemented"

        return text
