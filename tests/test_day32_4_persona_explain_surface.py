# tests/test_day32_4_persona_explain_surface.py

from core.persona.conversational_style_adapter import ConversationalStyleAdapter


def test_explain_fields_present_when_applied():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Explain test",
        persona_enabled=True,
        explain_trace=trace,
    )

    assert trace["persona.style_mode"] == "conversational_hindi"
    assert trace["persona.style_applied"] is True
    assert "persona.style_suffix" in trace
    assert "persona.style_reason" not in trace
    assert out.endswith(trace["persona.style_suffix"])


def test_explain_fields_present_when_persona_disabled():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Explain test",
        persona_enabled=False,
        explain_trace=trace,
    )

    assert trace["persona.style_mode"] == "conversational_hindi"
    assert trace["persona.style_applied"] is False
    assert trace["persona.style_reason"] == "persona_disabled"
    assert "persona.style_suffix" not in trace
    assert out == "Explain test"


def test_explain_fields_present_on_guard_violation():
    adapter = ConversationalStyleAdapter()
    trace = {}

    adapter._select_suffix = lambda _: " samjha Boss"  # invalid masculine

    out = adapter.apply(
        "Explain test",
        persona_enabled=True,
        explain_trace=trace,
    )

    assert trace["persona.style_applied"] is False
    assert trace["persona.style_reason"] == "guard_violation"
    assert "persona.style_suffix" not in trace
    assert out == "Explain test"
