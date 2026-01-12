import pytest
from dataclasses import FrozenInstanceError

from core.memory.influence.preference_schema import (
    PreferenceInfluence,
    PreferenceType,
    InfluenceStrength,
)


def test_schema_is_immutable():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.TONE,
        value="friendly",
    )
    with pytest.raises(FrozenInstanceError):
        pref.value = "formal"


def test_enum_bounds_enforced():
    assert PreferenceType.TONE.value == "tone"
    assert PreferenceType.VERBOSITY.value == "verbosity"
    assert InfluenceStrength.SOFT.value == "soft"
    assert InfluenceStrength.NONE.value == "none"


def test_is_active_true_for_soft():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.VERBOSITY,
        value="high",
        strength=InfluenceStrength.SOFT,
    )
    assert pref.is_active() is True


def test_is_active_false_for_none():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.FORMAT,
        value="bullets",
        strength=InfluenceStrength.NONE,
    )
    assert pref.is_active() is False


def test_explain_is_deterministic():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.LANGUAGE,
        value="en",
        strength=InfluenceStrength.SOFT,
        source="memory",
    )
    explanation = pref.explain()
    assert explanation == (
        "Preference influence detected: language = 'en' "
        "(strength=soft, source=memory)"
    )


def test_only_valid_preference_types_allowed():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.THEME,
        value="dark",
    )
    assert pref.pref_type == PreferenceType.THEME
