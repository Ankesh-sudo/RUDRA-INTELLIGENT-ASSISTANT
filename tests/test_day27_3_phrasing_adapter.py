from core.response.phrasing_adapter import PhrasingAdapter
from core.memory.influence.preference_schema import (
    PreferenceInfluence,
    PreferenceType,
    InfluenceStrength,
)
from core.memory.influence.weighting import InfluenceWeight


BASE_TEXT = "You can open the file. It will appear on the screen."


def test_no_influence_returns_identical_text():
    adapted, explanations = PhrasingAdapter.adapt(
        text=BASE_TEXT,
        influences=[],
        weight=None,
    )
    assert adapted == BASE_TEXT
    assert explanations == []


def test_tone_formal_changes_wording_only():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.TONE,
        value="formal",
        strength=InfluenceStrength.SOFT,
    )
    adapted, explanations = PhrasingAdapter.adapt(
        text=BASE_TEXT,
        influences=[pref],
    )
    assert "the user" in adapted
    assert adapted.endswith("screen.")
    assert explanations


def test_verbosity_low_reduces_text():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.VERBOSITY,
        value="low",
        strength=InfluenceStrength.SOFT,
    )
    adapted, _ = PhrasingAdapter.adapt(
        text=BASE_TEXT,
        influences=[pref],
    )
    assert adapted.count(".") == 1


def test_format_bullets_converts_safely():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.FORMAT,
        value="bullets",
        strength=InfluenceStrength.SOFT,
    )
    adapted, _ = PhrasingAdapter.adapt(
        text=BASE_TEXT,
        influences=[pref],
    )
    assert adapted.startswith("- ")
    assert "\n- " in adapted


def test_language_and_theme_are_ignored_safely():
    pref_lang = PreferenceInfluence(
        pref_type=PreferenceType.LANGUAGE,
        value="en",
        strength=InfluenceStrength.SOFT,
    )
    pref_theme = PreferenceInfluence(
        pref_type=PreferenceType.THEME,
        value="dark",
        strength=InfluenceStrength.SOFT,
    )
    adapted, explanations = PhrasingAdapter.adapt(
        text=BASE_TEXT,
        influences=[pref_lang, pref_theme],
    )
    assert adapted == BASE_TEXT
    assert explanations == []


def test_weight_explanation_is_added():
    weight = InfluenceWeight(value=0.2)
    adapted, explanations = PhrasingAdapter.adapt(
        text=BASE_TEXT,
        influences=[],
        weight=weight,
    )
    assert adapted == BASE_TEXT
    assert explanations == [weight.explain()]


def test_deterministic_output():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.VERBOSITY,
        value="low",
        strength=InfluenceStrength.SOFT,
    )
    out1, _ = PhrasingAdapter.adapt(BASE_TEXT, [pref])
    out2, _ = PhrasingAdapter.adapt(BASE_TEXT, [pref])
    assert out1 == out2
