from core.persona_maturity.persona_guardrails import PersonaGuardrails
from core.persona_maturity.persona_mode import PersonaMode


def test_guardrails_accepts_clean_text():
    result = PersonaGuardrails.validate(
        "Hello. How can I help?",
        PersonaMode.NEUTRAL,
    )
    assert result.approved is True


def test_guardrails_rejects_forbidden_phrase():
    result = PersonaGuardrails.validate(
        "You need me to succeed.",
        PersonaMode.BEST_FRIEND,
    )
    assert result.approved is False
