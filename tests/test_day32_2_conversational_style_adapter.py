# tests/test_day32_2_conversational_style_adapter.py

from core.persona.conversational_style_adapter import ConversationalStyleAdapter


def test_persona_disabled_noop():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Hello",
        persona_enabled=False,
        explain_trace=trace,
    )

    assert out == "Hello"
    assert trace["persona.style_applied"] is False


def test_persona_enabled_suffix_added():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Hello",
        persona_enabled=True,
        explain_trace=trace,
    )

    assert out.startswith("Hello")
    assert out != "Hello"
    assert trace["persona.style_applied"] is True


def test_suffix_is_whitelisted():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Test message",
        persona_enabled=True,
        explain_trace=trace,
    )

    suffix = out[len("Test message") :]
    assert suffix in adapter._SUFFIXES


def test_prefix_unchanged():
    adapter = ConversationalStyleAdapter()
    trace = {}

    text = "Exact prefix"
    out = adapter.apply(
        text,
        persona_enabled=True,
        explain_trace=trace,
    )

    assert out.startswith(text)


def test_deterministic_output():
    adapter = ConversationalStyleAdapter()
    trace1 = {}
    trace2 = {}

    out1 = adapter.apply(
        "Determinism",
        persona_enabled=True,
        explain_trace=trace1,
    )
    out2 = adapter.apply(
        "Determinism",
        persona_enabled=True,
        explain_trace=trace2,
    )

    assert out1 == out2
