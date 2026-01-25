from dataclasses import dataclass
from enum import Enum

from core.persona_maturity.persona_freeze import PersonaFreeze
from core.emotional_safety.safety_decision import SafetyOutcome
from .authority_lock import AuthorityLock


class AuthorityOutcome(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


@dataclass(frozen=True)
class AuthorityDecision:
    outcome: AuthorityOutcome
    reason: str


class AuthorityGuard:
    """
    Final enforcement gate for persona output.
    """

    @staticmethod
    def check(
        *,
        emotional_safety_outcome: SafetyOutcome,
    ) -> AuthorityDecision:

        # Persona maturity must be frozen
        try:
            PersonaFreeze.assert_frozen()
        except RuntimeError:
            return AuthorityDecision(
                outcome=AuthorityOutcome.BLOCK,
                reason="Persona maturity not frozen",
            )

        # Emotional safety must allow
        if emotional_safety_outcome != SafetyOutcome.ALLOW:
            return AuthorityDecision(
                outcome=AuthorityOutcome.BLOCK,
                reason="Emotional safety veto",
            )

        # Authority lock must be active
        try:
            AuthorityLock.assert_locked()
        except RuntimeError:
            return AuthorityDecision(
                outcome=AuthorityOutcome.BLOCK,
                reason="Authority lock inactive",
            )

        return AuthorityDecision(
            outcome=AuthorityOutcome.ALLOW,
            reason="Persona output permitted",
        )
