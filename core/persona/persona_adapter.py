from datetime import datetime
from typing import Tuple

from core.persona.persona_contract import PersonaInput
from core.persona.persona_trace import PersonaTrace
from core.persona.persona_guard import PersonaGuard
from core.persona.persona_expressiveness import PersonaExpressiveness
from core.persona.persona_toggle import PersonaToggle


class PersonaAdapter:
    """
    Persona adapter — Day 31.4

    Guarantees:
    - Persona is optional (toggleable)
    - Persona failure is silent
    - Persona never blocks output
    """

    PERSONA_NAME = "maahi"

    @classmethod
    def apply(cls, persona_input: PersonaInput) -> Tuple[str, PersonaTrace | None]:
        original_text = persona_input.text
        tone = persona_input.tone_hint or "neutral"

        # Persona OFF → hard bypass
        if not PersonaToggle.is_enabled():
            return original_text, None

        try:
            transformed_text = PersonaExpressiveness.apply_suffix(
                original_text,
                tone,
            )

            # Guard 1: prefix must be preserved
            if not PersonaGuard.is_prefix_preserved(
                original_text,
                transformed_text,
            ):
                raise ValueError("Persona prefix violation")

            # Guard 2: semantic core unchanged
            if not PersonaGuard.is_semantically_safe(
                original_text,
                original_text,
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
            # Fail-closed fallback
            trace = PersonaTrace(
                persona_name=cls.PERSONA_NAME,
                original_text=original_text,
                transformed_text=original_text,
                tone_applied="fallback",
                timestamp=datetime.utcnow(),
            )
            return original_text, trace
