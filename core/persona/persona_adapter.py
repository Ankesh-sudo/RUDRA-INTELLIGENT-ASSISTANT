from typing import Optional, Dict

from core.persona.profile import PersonaProfile
from core.persona.persona_lock import PersonaLock
from core.persona.conversational_style_adapter import ConversationalStyleAdapter


class PersonaAdapter:
    """
    Persona Adapter — Day 36.5 (SEALED)

    Guarantees:
    - Persona is cosmetic only (suffix-only)
    - Persona has NO authority
    - Persona is applied exactly once
    - Persona sees ONLY final approved text
    - Persona validation is strict
    - Cosmetic failures never downgrade persona
    - Persona explain schema is STABLE
    """

    @staticmethod
    def apply(
        final_text: str,
        persona: Optional[PersonaProfile],
        explain: Optional[Dict] = None,
    ) -> str:

        # No persona → hard bypass
        if persona is None:
            return final_text

        # ---- STRICT VALIDATION (only this may fail persona) ----
        try:
            PersonaLock.validate(persona)
        except Exception:
            if explain is not None:
                explain["persona"] = {
                    "name": persona.name,
                    "version": persona.version,
                    "fingerprint": persona.fingerprint(),
                    "affection_tier": persona.affection_tier,
                    "applied": False,
                    "reason": "persona_validation_failed",
                }
            return final_text

        # ---- COSMETIC APPLICATION (never fails persona) ----
        try:
            styled_text = ConversationalStyleAdapter.apply(
                text=final_text,
                suffixes=persona.suffixes,
            )
        except Exception:
            styled_text = final_text  # cosmetic failure ignored

        if explain is not None:
            explain["persona"] = {
                "name": persona.name,
                "version": persona.version,
                "fingerprint": persona.fingerprint(),
                "affection_tier": persona.affection_tier,
                "applied": True,
            }

        return styled_text
