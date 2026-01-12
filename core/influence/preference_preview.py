from dataclasses import dataclass
from typing import Dict, List

from core.influence.preference_resolution import ResolvedPreference


@dataclass(frozen=True)
class PreferencePreview:
    """
    Read-only preview of a resolved preference.
    No execution. No mutation.
    """
    key: str
    value: object
    scope: object
    status: str  # 'eligible' only for Day 29.2
    effect: str  # human hint (non-binding)


def build_previews(
    resolved: Dict[str, ResolvedPreference],
    *,
    context: str,
) -> List[PreferencePreview]:
    """
    Build non-binding previews based on declared scope.
    Filters by context only (no exclusions yet).
    """
    previews: List[PreferencePreview] = []

    for key, pref in resolved.items():
        if pref.scope.contexts and context not in pref.scope.contexts:
            continue

        previews.append(
            PreferencePreview(
                key=key,
                value=pref.value,
                scope=pref.scope,
                status="eligible",
                effect=_describe_effect(key, pref.value),
            )
        )

    return previews


def _describe_effect(key: str, value: object) -> str:
    # Human hint only. No guarantees.
    if key == "verbosity" and value == "short":
        return "shorten response"
    if key == "verbosity" and value == "long":
        return "expand response"
    if key == "format" and value == "bullet":
        return "format response as bullets"
    return "affect output phrasing"
