from typing import Dict, List, Any
from core.influence.resolved_preferences import (
    ResolvedPreferenceSet,
    PreferenceResolutionRecord,
)

SOURCE_PRIORITY = {
    "session": 3,
    "scoped": 2,
    "stored": 1,
}


def _stable_sort_key(pref: Dict[str, Any]):
    return (
        -SOURCE_PRIORITY.get(pref["source"], 0),
        -pref.get("timestamp", 0),
        pref["value"],
    )


def resolve_preferences(
    detected_preferences: List[Dict[str, Any]],
    session_preferences: List[Dict[str, Any]],
    scoped_preferences: List[Dict[str, Any]],
    stored_preferences: List[Dict[str, Any]],
) -> ResolvedPreferenceSet:
    """
    Resolve preferences deterministically.
    No mutation. No side effects.
    """

    all_prefs: Dict[str, List[Dict[str, Any]]] = {}

    for pref in (
        detected_preferences
        + session_preferences
        + scoped_preferences
        + stored_preferences
    ):
        key = pref["key"]
        all_prefs.setdefault(key, []).append(pref)

    resolved: Dict[str, PreferenceResolutionRecord] = {}

    for key in sorted(all_prefs.keys()):
        candidates = all_prefs[key]
        sorted_candidates = sorted(candidates, key=_stable_sort_key)

        winner = sorted_candidates[0]
        rejected = sorted_candidates[1:]

        record = PreferenceResolutionRecord(
            key=key,
            value=winner["value"],
            source=winner["source"],
            reason=_resolution_reason(winner, rejected),
            rejected=[
                {
                    "value": r["value"],
                    "source": r["source"],
                    "reason": "lower priority or older",
                }
                for r in rejected
            ],
        )

        resolved[key] = record

    return ResolvedPreferenceSet(preferences=resolved)


def _resolution_reason(winner: Dict[str, Any], rejected: List[Dict[str, Any]]) -> str:
    if not rejected:
        return f"only available preference from {winner['source']}"

    return f"{winner['source']} preference overrides lower-priority sources"
