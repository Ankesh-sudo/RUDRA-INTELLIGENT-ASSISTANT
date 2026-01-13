# core/persona/conversational_style_adapter.py

from typing import Dict, List
import hashlib


class ConversationalStyleAdapter:
    """
    Applies cosmetic, suffix-only conversational style.
    Meaning-preserving and non-authoritative.
    """

    _SUFFIXES: List[str] = [
        " 🙂",
        " Boss 😊",
        " samajh gayi Boss 🙂",
        " theek hai Boss 😊",
        " bilkul samajh gayi Boss 🙂",
    ]

    def apply(
        self,
        text: str,
        *,
        persona_enabled: bool,
        explain_trace: Dict,
    ) -> str:
        # Persona disabled → strict no-op
        if not persona_enabled:
            explain_trace["persona.style_applied"] = False
            explain_trace["persona.style_mode"] = "conversational_hindi"
            explain_trace["persona.style_reason"] = "persona_disabled"
            return text

        # Deterministic suffix selection
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        index = int(digest, 16) % len(self._SUFFIXES)
        suffix = self._SUFFIXES[index]

        styled = text + suffix

        explain_trace["persona.style_applied"] = True
        explain_trace["persona.style_mode"] = "conversational_hindi"
        explain_trace["persona.style_suffix"] = suffix

        return styled
