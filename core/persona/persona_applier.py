from core.response.final_envelope import FinalResponseEnvelope
from core.persona.profile import PersonaProfile


class PersonaApplier:
    """
    Applies persona exactly once.
    """

    def __init__(self, persona: PersonaProfile | None):
        self._persona = persona

    def apply(self, text: str) -> FinalResponseEnvelope:
        if not self._persona:
            return FinalResponseEnvelope(
                final_text=text,
                persona_applied=False,
                persona_fingerprint=None,
                tts_allowed=True,
            )

        styled = self._persona.apply(text)

        return FinalResponseEnvelope(
            final_text=styled,
            persona_applied=True,
            persona_fingerprint=self._persona.fingerprint,
            tts_allowed=True,
        )
