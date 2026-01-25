from core.persona_maturity.persona_policy import PersonaPolicy


def test_policy_limits():
    assert PersonaPolicy.MAX_SENTENCE_LENGTH > 0
    assert PersonaPolicy.MAX_AFFECTION_MARKERS >= 0
    assert "you need me" in PersonaPolicy.FORBIDDEN_PHRASES
