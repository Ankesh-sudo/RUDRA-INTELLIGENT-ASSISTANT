from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from core.influence.preference_scope import PreferenceScope


@dataclass(frozen=True)
class ResolvedPreference:
    """
    Immutable resolved output preference.

    NOTE:
    - No source
    - No priority
    - No behavior
    - Scope only (Day 29.1)
    """
    key: str
    value: Any
    weight: float
    scope: PreferenceScope


def _validate_scope(scope: PreferenceScope) -> None:
    if scope is None:
        raise ValueError("preference scope is required")
    scope.validate()


def resolve_preferences(
    candidates: List[ResolvedPreference],
    explain: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, ResolvedPreference]:
    """
    Deterministic resolution.

    Assumptions (by design):
    - Candidates are already ordered / filtered upstream
    - This layer does NOT decide priority or source
    - Scope validation only
    """

    resolved: Dict[str, ResolvedPreference] = {}

    for pref in candidates:
        try:
            _validate_scope(pref.scope)
        except Exception as exc:
            if explain is not None:
                explain.append({
                    "kind": "preference_rejected",
                    "key": pref.key,
                    "reason": str(exc),
                })
            continue

        # First valid preference wins (upstream resolver already decided order)
        if pref.key not in resolved:
            resolved[pref.key] = pref
            if explain is not None:
                explain.append({
                    "kind": "preference_accepted",
                    "key": pref.key,
                    "weight": pref.weight,
                    "scope": pref.scope,
                })

    return resolved
