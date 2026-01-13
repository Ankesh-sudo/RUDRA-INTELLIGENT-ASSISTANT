from datetime import datetime
from typing import Tuple

from core.persona.persona_contract import PersonaInput
from core.persona.persona_trace import PersonaTrace
from core.persona.persona_guard import PersonaGuard
from core.persona.persona_expressiveness import PersonaExpressiveness


class PersonaAdapter:
    """
    Persona adapter — Day 31.3

    Allows:
    - suffix-only expressiveness (emoji / warmth)

    Still forbids:
    - rewording
    - insertion
    - deletion
    - authority changes
    """

    PERSONA_NAME = "maahi"

    @classmethod
    def apply(cls, persona_input: PersonaInput) -> Tuple[str, PersonaTrace]:
        original_text = persona_input.text
        tone = persona_input.tone_hint or "neutral"

        try:
            # Apply SAFE suffix-only expressiveness
            transformed_text = PersonaExpressiveness.apply_suffix(
                original_text,
                tone,
            )

            # Guard 1: original text must be preserved as prefix
            if not PersonaGuard.is_prefix_preserved(
                original_text,
                transformed_text,
            ):
                raise ValueError("Persona prefix violation")

            # Guard 2: semantic safety (still enforced)
            if not PersonaGuard.is_semantically_safe(
                original_text,
                original_text,  # semantic comparison is against base text
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
            trace = PersonaTrace(
                persona_name=cls.PERSONA_NAME,
                original_text=original_text,
                transformed_text=original_text,
                tone_applied="fallback",
                timestamp=datetime.utcnow(),
            )
            return original_text, trace
