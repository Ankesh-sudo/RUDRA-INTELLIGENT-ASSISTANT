from core.influence.output_preferences import (
    build_output_preferences,
    OutputPreferences,
)
from core.influence.resolved_preferences import (
    ResolvedPreferenceSet,
    PreferenceResolutionRecord,
)
from core.explain.formatter import apply_output_preferences


def resolved_pref(key, value):
    return PreferenceResolutionRecord(
        key=key,
        value=value,
        source="session",
        reason="test",
        rejected=[],
    )


def test_empty_resolved_preferences():
    resolved = ResolvedPreferenceSet(preferences={})
    output = build_output_preferences(resolved)
    assert output.is_empty()


def test_whitelisted_preference_exposed():
    resolved = ResolvedPreferenceSet(
        preferences={
            "verbosity": resolved_pref("verbosity", "short"),
        }
    )
    output = build_output_preferences(resolved)
    assert output.verbosity == "short"


def test_non_whitelisted_preference_ignored():
    resolved = ResolvedPreferenceSet(
        preferences={
            "color": resolved_pref("color", "red"),
        }
    )
    output = build_output_preferences(resolved)
    assert output.is_empty()


def test_no_preference_no_change():
    text = "This is a test sentence. Another sentence."
    result = apply_output_preferences(text, OutputPreferences())
    assert result == text


def test_verbosity_short_applied():
    text = "This is a test sentence. Another sentence."
    prefs = OutputPreferences(verbosity="short")
    result = apply_output_preferences(text, prefs)
    assert result == "This is a test sentence."


def test_format_bullet_applied():
    text = "First sentence. Second sentence."
    prefs = OutputPreferences(format="bullet")
    result = apply_output_preferences(text, prefs)
    assert result.startswith("- ")
