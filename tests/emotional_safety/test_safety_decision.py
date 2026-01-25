from core.emotional_safety.safety_decision import SafetyDecision, SafetyOutcome


def test_zero_tolerance_blocks():
    decision = SafetyDecision.decide(["only me"])
    assert decision.outcome == SafetyOutcome.BLOCK


def test_allow_clean_text():
    decision = SafetyDecision.decide([])
    assert decision.outcome == SafetyOutcome.ALLOW
