from core.emotional_safety.safety_explain import SafetyExplain
from core.emotional_safety.safety_decision import SafetyDecision, SafetyOutcome


def test_explain_structure():
    decision = SafetyDecision(
        outcome=SafetyOutcome.BLOCK,
        reason="Test reason",
    )
    info = SafetyExplain.explain(
        text="only me",
        detected_signals=["only me"],
        decision=decision,
    )

    assert info["outcome"] == "block"
    assert "reason" in info
