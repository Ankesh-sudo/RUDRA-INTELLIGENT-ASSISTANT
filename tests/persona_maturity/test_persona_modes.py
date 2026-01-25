from core.persona_maturity.persona_mode import PersonaMode


def test_persona_modes_exist():
    assert PersonaMode.NEUTRAL.value == "neutral"
    assert PersonaMode.BEST_FRIEND.value == "best_friend"
    assert PersonaMode.WARRIOR.value == "warrior"
