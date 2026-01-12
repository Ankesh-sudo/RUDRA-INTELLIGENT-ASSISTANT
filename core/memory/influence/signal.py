from dataclasses import dataclass
from enum import Enum
from typing import Optional


class InfluenceStrength(str, Enum):
    LOW = "low"
    MEDIUM = "medium"


class InfluenceCategory(str, Enum):
    PREFERENCE = "preference"
    HABIT = "habit"
    CONTEXT = "context"


@dataclass(frozen=True)
class InfluenceSignal:
    """
    Immutable advisory signal derived from memory recall.
    This object must NEVER alter logic or execution.
    """
    source_memory_id: str
    category: InfluenceCategory
    strength: InfluenceStrength
    message: str
    permit_id: str
    scope: Optional[str] = None  # session / once / scoped
