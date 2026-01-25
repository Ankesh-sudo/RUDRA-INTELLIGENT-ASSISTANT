from core.persona_authority.authority_explain import AuthorityExplain
from core.persona_authority.authority_guard import AuthorityDecision, AuthorityOutcome


def test_authority_explain_output():
    decision = AuthorityDecision(
        outcome=AuthorityOutcome.BLOCK,
        reason="Test block",
    )

    info = AuthorityExplain.explain(decision)

    assert info["authority_lock_active"] is True
    assert info["outcome"] == "block"
    assert info["reason"] == "Test block"
