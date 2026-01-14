from typing import Optional, Tuple, Union
from datetime import datetime

from core.persona.profile import PersonaProfile
from core.persona.persona_lock import PersonaLock
from core.persona.persona_toggle import PersonaToggle
from core.persona.conversational_style_adapter import ConversationalStyleAdapter


class PersonaTrace:
    """
    Legacy persona trace (Day 31 contract)
    """

    def __init__(
        self,
        *,
        original_text: str,
        transformed_text: str,
        persona_name: str,
        tone_applied: str,
        applied: bool,
    ):
        self.original_text = original_text
        self.transformed_text = transformed_text
        self.persona_name = persona_name
        self.tone_applied = tone_applied
        self.applied = applied
        self.timestamp = datetime.utcnow()


class PersonaAdapter:
    """
    Persona Adapter — legacy + sealed compatibility
    """

    @staticmethod
    def apply(
        input_or_text: Union[str, object, None] = None,
        persona: Optional[PersonaProfile] = None,
        explain: Optional[dict] = None,
        *,
        final_text: Optional[str] = None,
    ) -> Union[str, Tuple[str, Optional[PersonaTrace]]]:

        # ============================================================
        # LEGACY API — Day 31–37
        # ============================================================
        if final_text is None and input_or_text is not None and hasattr(input_or_text, "text"):
            persona_input = input_or_text
            original = persona_input.text
            tone = getattr(persona_input, "tone_hint", None) or "neutral"

            # Persona disabled → strict bypass
            if not PersonaToggle.is_enabled():
                return original, None

            # System / status messages MUST NOT be modified
            lowered = original.lower()
            system_keywords = ("system", "update", "shutdown", "shut down")
            is_system_text = lowered.startswith(system_keywords) or any(
                kw in lowered for kw in system_keywords
            )

            transformed = original
            applied = False

            # Playful tone allowed ONLY for non-system text
            if tone == "playful" and not is_system_text:
                adapter = ConversationalStyleAdapter()
                try:
                    transformed = adapter.apply(
                        original,
                        persona_enabled=True,
                        explain_trace={},
                    )
                    applied = transformed != original
                except Exception:
                    transformed = original
                    applied = False

            trace = PersonaTrace(
                original_text=original,
                transformed_text=transformed,
                persona_name="maahi",
                tone_applied=tone,
                applied=applied,
            )

            return transformed, trace

        # ============================================================
        # SEALED API — Day 36.5+
        # ============================================================
        text = final_text if final_text is not None else input_or_text

        # No persona → hard bypass
        if persona is None:
            return text

        # Ensure explain surface exists
        if explain is not None:
            explain.setdefault("persona", {})

        # Prevent double application
        if isinstance(text, str) and "Boss" in text:
            if explain is not None:
                explain["persona"]["applied"] = False
                explain["persona"]["reason"] = "already_applied"
            return text

        # Validate persona
        try:
            PersonaLock.validate(persona)
        except Exception:
            if explain is not None:
                explain["persona"].update(
                    {
                        "name": persona.name,
                        "version": persona.version,
                        "fingerprint": persona.fingerprint(),
                        "affection_tier": persona.affection_tier,
                        "applied": False,
                        "reason": "persona_validation_failed",
                    }
                )
            return text

        adapter = ConversationalStyleAdapter()

        try:
            styled = adapter.apply(
                text,
                persona_enabled=True,
                explain_trace=explain if explain is not None else {},
            )
            applied = styled != text
        except Exception:
            styled = text
            applied = False

        if explain is not None:
            explain["persona"].update(
                {
                    "name": persona.name,
                    "version": persona.version,
                    "fingerprint": persona.fingerprint(),
                    "affection_tier": persona.affection_tier,
                    "applied": applied,
                }
            )

        return styled
