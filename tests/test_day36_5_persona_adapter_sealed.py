# tests/test_day36_5_persona_adapter_sealed.py

from core.persona.persona_adapter import PersonaAdapter
from core.persona.persona_registry import MAAHI_PROFILE
from core.persona.profile import PersonaProfile


def test_persona_applied_exactly_once():
    text = "Playing your playlist"
    explain = {}

    first = PersonaAdapter.apply(
        final_text=text,
        persona=MAAHI_PROFILE,
        explain=explain,
    )

    second = PersonaAdapter.apply(
        final_text=first,
        persona=MAAHI_PROFILE,
        explain={},
    )

    # Suffix must appear only once
    assert second.count("🙂") <= 1


def test_persona_none_is_hard_bypass():
    text = "Open Firefox"

    result = PersonaAdapter.apply(
        final_text=text,
        persona=None,
        explain={},
    )

    assert result == text


def test_persona_failure_falls_back_safely():
    bad_profile = PersonaProfile(
        name="Maahi",
        version="1.0",
        affection_tier="B",  # illegal
        suffixes=(" ❤️",),
    )

    text = "Sending message"
    explain = {}

    result = PersonaAdapter.apply(
        final_text=text,
        persona=bad_profile,
        explain=explain,
    )

    assert result == text
    assert explain["persona"]["applied"] is False


def test_persona_explain_trace_is_cosmetic_only():
    text = "Playing music"
    explain = {}

    PersonaAdapter.apply(
        final_text=text,
        persona=MAAHI_PROFILE,
        explain=explain,
    )

    persona_trace = explain.get("persona")
    assert persona_trace is not None

    assert persona_trace["name"] == "Maahi"
    assert persona_trace["affection_tier"] == "A"
    assert persona_trace["applied"] is True

    forbidden_keys = {"intent", "memory", "confidence", "action"}
    assert forbidden_keys.isdisjoint(persona_trace.keys())
