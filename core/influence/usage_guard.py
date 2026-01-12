from typing import Optional, Tuple
from core.influence.usage_state import PreferenceUsageState
from core.influence.output_preferences import OutputPreferences


def guard_output_preferences(
    output_prefs: OutputPreferences,
    usage_state: PreferenceUsageState,
    current_session_id: str,
) -> Tuple[Optional[OutputPreferences], dict]:
    """
    Single authoritative gate before applying output preferences.
    Returns (allowed_output_prefs | None, explain_event).
    """

    if usage_state.is_expired(current_session_id):
        return None, {
            "kind": "output_preference_blocked",
            "reason": "session expired or disabled",
        }

    if output_prefs.is_empty():
        return None, {
            "kind": "output_preference_blocked",
            "reason": "no preferences to apply",
        }

    return output_prefs, {
        "kind": "output_preference_allowed",
        "reason": usage_state.reason,
    }
