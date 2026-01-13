# core/persona/persona_lock.py

from core.persona.profile import PersonaProfile


class PersonaLock:
    """
    Hard safety lock for persona invariants.
    Fail-fast by design.
    """

    @staticmethod
    def validate(profile: PersonaProfile) -> None:
        """
        Enforces non-escalation guarantees.
        """
        if profile.affection_tier != "A":
            raise RuntimeError(
                f"Persona affection tier escalation blocked: {profile.affection_tier}"
            )
