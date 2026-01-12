from dataclasses import dataclass
from enum import Enum
from typing import Optional


class InfluenceGateDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class InfluenceGateResult:
    """
    Result of evaluating whether memory influence is permitted.
    Immutable and side-effect free.
    """
    decision: InfluenceGateDecision
    reason: str
    permit_id: Optional[str] = None


def evaluate_influence_gate(
    *,
    usage_mode: str,
    permit,
    recalled_memories: list,
) -> InfluenceGateResult:
    """
    Determines whether memory influence is allowed to be evaluated.

    Rules (deterministic, ordered):
    1. Usage mode must not be DISABLED
    2. Permit must exist
    3. Permit must explicitly allow influence
    4. Recalled memories must be present
    """

    # 1. Mode check
    if usage_mode == "DISABLED":
        return InfluenceGateResult(
            decision=InfluenceGateDecision.DENY,
            reason="memory usage mode is DISABLED",
        )

    # 2. Permit presence
    if permit is None:
        return InfluenceGateResult(
            decision=InfluenceGateDecision.DENY,
            reason="no memory permit provided",
        )

    # 3. Permit allows influence
    if not getattr(permit, "allow_influence", False):
        return InfluenceGateResult(
            decision=InfluenceGateDecision.DENY,
            reason="permit does not allow influence",
            permit_id=getattr(permit, "id", None),
        )

    # 4. Recall provenance
    if not recalled_memories:
        return InfluenceGateResult(
            decision=InfluenceGateDecision.DENY,
            reason="no recalled memories available for influence",
            permit_id=getattr(permit, "id", None),
        )

    # 5. Allowed
    return InfluenceGateResult(
        decision=InfluenceGateDecision.ALLOW,
        reason="memory influence allowed",
        permit_id=getattr(permit, "id", None),
    )
