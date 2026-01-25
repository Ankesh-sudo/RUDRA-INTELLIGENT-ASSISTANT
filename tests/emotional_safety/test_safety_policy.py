from core.emotional_safety.safety_policy import SafetyPolicy


def test_policy_limits():
    assert SafetyPolicy.MAX_SIGNAL_HITS >= 0
    assert SafetyPolicy.ZERO_TOLERANCE_ENABLED is True
