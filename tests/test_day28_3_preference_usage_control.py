from core.influence.usage_state import PreferenceUsageState
from core.influence.usage_guard import guard_output_preferences
from core.influence.output_preferences import OutputPreferences


def test_opt_out_blocks_preferences():
    prefs = OutputPreferences(verbosity="short")
    state = PreferenceUsageState.disabled("user opted out")

    allowed, event = guard_output_preferences(
        prefs, state, current_session_id="s1"
    )

    assert allowed is None
    assert event["kind"] == "output_preference_blocked"


def test_enabled_allows_preferences():
    prefs = OutputPreferences(verbosity="short")
    state = PreferenceUsageState.enabled_for_session("s1")

    allowed, event = guard_output_preferences(
        prefs, state, current_session_id="s1"
    )

    assert allowed == prefs
    assert event["kind"] == "output_preference_allowed"


def test_session_expiry_blocks_preferences():
    prefs = OutputPreferences(verbosity="short")
    state = PreferenceUsageState.enabled_for_session("s1")

    allowed, event = guard_output_preferences(
        prefs, state, current_session_id="s2"
    )

    assert allowed is None
    assert event["kind"] == "output_preference_blocked"


def test_empty_preferences_blocked_even_if_enabled():
    prefs = OutputPreferences()
    state = PreferenceUsageState.enabled_for_session("s1")

    allowed, event = guard_output_preferences(
        prefs, state, current_session_id="s1"
    )

    assert allowed is None
    assert event["kind"] == "output_preference_blocked"
