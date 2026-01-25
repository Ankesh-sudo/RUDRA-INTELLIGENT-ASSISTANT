from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ThoughtPlan:
    """
    Day 72 — Silent reasoning artifact.

    HARD RULES:
    - NEVER spoken
    - NEVER logged verbatim
    - NEVER stored in memory
    - NEVER passed to persona or TTS
    """

    intent: Optional[str]
    decision: str
    safety_notes: str = ""
