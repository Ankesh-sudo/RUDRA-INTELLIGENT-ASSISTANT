from core.persona_authority.authority_guard import AuthorityGuard, AuthorityOutcome
from core.emotional_safety.safety_decision import SafetyOutcome
from core.persona_maturity.persona_freeze import PersonaFreeze


def test_authority_blocks_if_not_frozen():
    # Simulate unfrozen state by resetting class (test isolation)
    PersonaFreeze._frozen = False

    decision = AuthorityGuard.check(
        emotional_safety_outcome=SafetyOutcome.ALLOW,
    )
    assert decision.outcome == AuthorityOutcome.BLOCK


def test_authority_blocks_on_emotional_veto():
    PersonaFreeze.freeze()

    decision = AuthorityGuard.check(
        emotional_safety_outcome=SafetyOutcome.BLOCK,
    )
    assert decision.outcome == AuthorityOutcome.BLOCK


def test_authority_allows_when_all_checks_pass():
    PersonaFreeze.freeze()

    decision = AuthorityGuard.check(
        emotional_safety_outcome=SafetyOutcome.ALLOW,
    )
    assert decision.outcome == AuthorityOutcome.ALLOW
