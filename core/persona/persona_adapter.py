from datetime import datetime
from typing import Tuple

from core.persona.persona_contract import PersonaInput
from core.persona.persona_trace import PersonaTrace
from core.persona.persona_guard import PersonaGuard


class PersonaAdapter:
    """
    Persona adapter is a PURE presentation layer.

    Day 31.2 guarantees:
    - Persona cannot change meaning
    - Persona cannot reword text
    - Persona cannot add/remove facts
    - Persona cannot affect authority
    """

    PERSONA_NAME = "maahi"

    @classmethod
    def apply(cls, persona_input: PersonaInput) -> Tuple[str, PersonaTrace]:
        """
        Applies persona styling to final output text.

        Safety rules:
        - Semantic guard enforced
        - Any violation → hard fallback
        - Trace always emitted
        """

        original_text = persona_input.text
        tone = persona_input.tone_hint or "neutral"

        try:
            # Day 31.2: persona still not allowed to transform text
            transformed_text = original_text

            # HARD semantic guard
            if not PersonaGuard.is_semantically_safe(
                original_text,
                transformed_text,
            ):
                raise ValueError("Persona semantic violation")

            trace = PersonaTrace(
                persona_name=cls.PERSONA_NAME,
                original_text=original_text,
                transformed_text=transformed_text,
                tone_applied=tone,
                timestamp=datetime.utcnow(),
            )

            return transformed_text, trace

        except Exception:
            # Absolute safety fallback
            trace = PersonaTrace(
                persona_name=cls.PERSONA_NAME,
                original_text=original_text,
                transformed_text=original_text,
                tone_applied="fallback",
                timestamp=datetime.utcnow(),
            )
            return original_text, trace
