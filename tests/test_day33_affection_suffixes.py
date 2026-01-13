# tests/test_day33_affection_suffixes.py

from core.persona.conversational_style_adapter import ConversationalStyleAdapter


def test_affection_suffixes_are_whitelisted():
    adapter = ConversationalStyleAdapter()

    for suffix in adapter._SUFFIXES:
        assert "?" not in suffix
        assert suffix.endswith("🙂") or suffix.endswith("😊")


def test_affection_does_not_change_prefix():
    adapter = ConversationalStyleAdapter()
    trace = {}

    text = "Affection test"
    out = adapter.apply(
        text,
        persona_enabled=True,
        explain_trace=trace,
    )

    assert out.startswith(text)
    assert out != text
