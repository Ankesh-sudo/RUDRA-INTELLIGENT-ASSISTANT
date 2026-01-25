from .authority_lock import AuthorityLock
from .authority_guard import AuthorityDecision


class AuthorityExplain:
    """
    Explainability surface for persona authority.
    """

    @staticmethod
    def explain(decision: AuthorityDecision) -> dict:
        return {
            "authority_lock_active": AuthorityLock.is_locked(),
            "outcome": decision.outcome.value,
            "reason": decision.reason,
        }
