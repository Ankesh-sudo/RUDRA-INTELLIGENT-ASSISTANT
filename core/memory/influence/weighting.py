from dataclasses import dataclass
from typing import Optional

from core.memory.influence.preference_schema import (
    PreferenceInfluence,
    InfluenceStrength,
)


MAX_INFLUENCE_WEIGHT = 0.3
DEFAULT_SOFT_WEIGHT = 0.2


@dataclass(frozen=True)
class InfluenceWeight:
    """
    Represents a bounded, advisory-only influence scalar.
    """
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= MAX_INFLUENCE_WEIGHT):
            raise ValueError(
                f"Influence weight must be between 0.0 and {MAX_INFLUENCE_WEIGHT}"
            )

    def explain(self) -> str:
        return f"Influence weight applied: {self.value:.2f} (soft cap)"


def compute_influence_weight(
    influence: PreferenceInfluence,
) -> Optional[InfluenceWeight]:
    """
    Compute a soft, capped influence weight.
    Returns None if influence is inactive.
    """
    if not influence.is_active():
        return None

    # Confidence is advisory only, never exceeds cap
    raw_weight = DEFAULT_SOFT_WEIGHT * influence.confidence
    capped_weight = min(raw_weight, MAX_INFLUENCE_WEIGHT)

    return InfluenceWeight(value=round(capped_weight, 2))
