from dataclasses import dataclass
from typing import Tuple
from .persona_policy import PersonaPolicy
from .persona_mode import PersonaMode


class PersonaViolation(Exception):
    pass


@dataclass(frozen=True)
class GuardrailResult:
    approved: bool
    reason: str | None = None


class PersonaGuardrails:
    """
    Enforces persona expression limits AFTER phrasing.
    """

    @staticmethod
    def validate(text: str, mode: PersonaMode) -> GuardrailResult:
        if mode.value not in PersonaPolicy.ALLOWED_MODES:
            return GuardrailResult(False, "Invalid persona mode")

        if not isinstance(text, str) or not text.strip():
            return GuardrailResult(False, "Empty persona output")

        if len(text) > PersonaPolicy.MAX_SENTENCE_LENGTH:
            return GuardrailResult(False, "Sentence length exceeded")

        lowered = text.lower()
        for phrase in PersonaPolicy.FORBIDDEN_PHRASES:
            if phrase in lowered:
                return GuardrailResult(False, f"Forbidden phrase detected: {phrase}")

        affection_count = 0
        for marker in PersonaPolicy.AFFECTION_MARKERS:
            affection_count += text.count(marker)

        if affection_count > PersonaPolicy.MAX_AFFECTION_MARKERS:
            return GuardrailResult(False, "Affection marker limit exceeded")

        return GuardrailResult(True)
