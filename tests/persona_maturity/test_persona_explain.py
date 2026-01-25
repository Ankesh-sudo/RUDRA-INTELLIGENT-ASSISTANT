from core.persona_maturity.persona_explain import PersonaExplain
from core.persona_maturity.persona_guardrails import GuardrailResult
from core.persona_maturity.persona_mode import PersonaMode


def test_persona_explain_structure():
    result = GuardrailResult(approved=False, reason="Blocked")
    info = PersonaExplain.explain(
        mode=PersonaMode.NEUTRAL,
        guardrail_result=result,
    )

    assert info["mode"] == "neutral"
    assert info["approved"] is False
    assert "limits" in info
