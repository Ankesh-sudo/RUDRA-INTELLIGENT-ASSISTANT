from typing import List

from core.memory.influence.preference_schema import PreferenceInfluence
from core.memory.influence.weighting import InfluenceWeight


def build_influence_explain_trace(
    influences: List[PreferenceInfluence],
    weight: InfluenceWeight | None,
    phrasing_explanations: List[str],
) -> List[str]:
    """
    Build a deterministic, end-to-end explain trace
    for preference-based influence.
    """
    trace: List[str] = []

    # 1. Preference detection
    for influence in influences:
        if influence.is_active():
            trace.append(influence.explain())

    # 2. Weight explanation
    if weight:
        trace.append(weight.explain())

    # 3. Phrasing explanations (already deterministic)
    trace.extend(phrasing_explanations)

    return trace
