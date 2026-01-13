# tests/test_day32_3_style_guard.py

from core.persona.conversational_style_adapter import ConversationalStyleAdapter


def test_guard_allows_valid_suffix():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Hello",
        persona_enabled=True,
        explain_trace=trace,
    )

    assert out != "Hello"
    assert trace["persona.style_applied"] is True


def test_guard_blocks_when_persona_disabled():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Hello",
        persona_enabled=False,
        explain_trace=trace,
    )

    assert out == "Hello"
    assert trace["persona.style_applied"] is False
    assert trace["persona.style_reason"] == "persona_disabled"


def test_guard_blocks_non_whitelisted_suffix():
    adapter = ConversationalStyleAdapter()
    trace = {}

    # monkey-patch to simulate bad suffix
    adapter._select_suffix = lambda _: " samjha Boss"  # masculine, invalid

    out = adapter.apply(
        "Hello",
        persona_enabled=True,
        explain_trace=trace,
    )

    assert out == "Hello"
    assert trace["persona.style_applied"] is False
    assert trace["persona.style_reason"] == "guard_violation"


def test_prefix_byte_for_byte_preserved():
    adapter = ConversationalStyleAdapter()
    trace = {}

    text = "ExactPrefix✓"
    out = adapter.apply(
        text,
        persona_enabled=True,
        explain_trace=trace,
    )

    assert out.startswith(text)
    assert out[: len(text)] == text


def test_exactly_one_suffix_only():
    adapter = ConversationalStyleAdapter()
    trace = {}

    out = adapter.apply(
        "Once",
        persona_enabled=True,
        explain_trace=trace,
    )

    suffix = out[len("Once") :]
    assert suffix in adapter._SUFFIXES
