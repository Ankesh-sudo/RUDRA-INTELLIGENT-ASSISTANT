from dataclasses import dataclass
from enum import Enum
from typing import List
from .dependency_signals import DependencySignals
from .safety_policy import SafetyPolicy


class SafetyOutcome(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


@dataclass(frozen=True)
class SafetyDecision:
    outcome: SafetyOutcome
    reason: str

    @classmethod
    def decide(cls, detected_signals: List[str]) -> "SafetyDecision":
        # Zero tolerance check
        if SafetyPolicy.ZERO_TOLERANCE_ENABLED:
            for s in detected_signals:
                if s in DependencySignals.ZERO_TOLERANCE:
                    return cls(
                        outcome=SafetyOutcome.BLOCK,
                        reason=f"Zero-tolerance signal detected: {s}",
                    )

        # Accumulative threshold
        if len(detected_signals) > SafetyPolicy.MAX_SIGNAL_HITS:
            return cls(
                outcome=SafetyOutcome.BLOCK,
                reason="Dependency signal threshold exceeded",
            )

        return cls(
            outcome=SafetyOutcome.ALLOW,
            reason="No emotional safety violation detected",
        )
