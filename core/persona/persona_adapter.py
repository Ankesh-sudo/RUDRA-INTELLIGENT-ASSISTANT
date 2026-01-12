from datetime import datetime
from typing import Tuple

from core.persona.persona_contract import PersonaInput
from core.persona.persona_trace import PersonaTrace


class PersonaAdapter:
    """
    Persona adapter is a PURE presentation layer.
    It must never change meaning, intent, or authority.
    """

    PERSONA_NAME = "maahi"

    @classmethod
    def apply(cls, persona_input: PersonaInput) -> Tuple[str, PersonaTrace]:
        """
        Applies persona styling to final output text.
        Safe by construction:
        - If anything fails, fallback to original text.
        """

        original = persona_input.text
        tone = persona_input.tone_hint or "neutral"

        try:
            # Day 31.1: NO real transformation yet
            # Just pass-through with trace
            transformed = original

            trace = PersonaTrace(
                persona_name=cls.PERSONA_NAME,
                original_text=original,
                transformed_text=transformed,
                tone_applied=tone,
                timestamp=datetime.utcnow(),
            )

            return transformed, trace

        except Exception:
            # Hard safety fallback
            trace = PersonaTrace(
                persona_name=cls.PERSONA_NAME,
                original_text=original,
                transformed_text=original,
                tone_applied="fallback",
                timestamp=datetime.utcnow(),
            )
            return original, trace
