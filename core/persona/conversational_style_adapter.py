# core/persona/conversational_style_adapter.py

from typing import Dict, List
import hashlib


class ConversationalStyleAdapter:
    """
    Applies cosmetic, suffix-only conversational style.
    Meaning-preserving, non-authoritative, fail-closed.
    """

    _SUFFIXES: List[str] = [
        " 🙂",
        " Boss 😊",
        " samajh gayi Boss 🙂",
        " theek hai Boss 😊",
        " bilkul samajh gayi Boss 🙂",
    ]

    def _select_suffix(self, text: str) -> str:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        index = int(digest, 16) % len(self._SUFFIXES)
        return self._SUFFIXES[index]

    def _guard(
        self,
        original: str,
        candidate: str,
        suffix: str,
    ) -> bool:
        # must be original + suffix exactly
        if candidate != original + suffix:
            return False
        # exactly one suffix and whitelisted
        if suffix not in self._SUFFIXES:
            return False
        # prefix must be byte-for-byte identical
        if not candidate.startswith(original):
            return False
        return True

    def apply(
        self,
        text: str,
        *,
        persona_enabled: bool,
        explain_trace: Dict,
    ) -> str:
        explain_trace["persona.style_mode"] = "conversational_hindi"

        # Persona disabled → strict no-op
        if not persona_enabled:
            explain_trace["persona.style_applied"] = False
            explain_trace["persona.style_reason"] = "persona_disabled"
            return text

        suffix = self._select_suffix(text)
        candidate = text + suffix

        if not self._guard(text, candidate, suffix):
            explain_trace["persona.style_applied"] = False
            explain_trace["persona.style_reason"] = "guard_violation"
            return text

        explain_trace["persona.style_applied"] = True
        explain_trace["persona.style_suffix"] = suffix
        return candidate
