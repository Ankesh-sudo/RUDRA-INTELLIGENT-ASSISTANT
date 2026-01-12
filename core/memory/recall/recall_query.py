from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.memory.types import MemoryCategory
from .exceptions import InvalidRecallQuery


class MatchMode(Enum):
    EXACT = "exact"
    CONTAINS = "contains"


@dataclass(frozen=True)
class RecallQuery:
    category: Optional[MemoryCategory] = None
    text: Optional[str] = None
    min_confidence: float = 0.0
    match_mode: MatchMode = MatchMode.CONTAINS
    limit: Optional[int] = None

    def __post_init__(self):
        if not 0.0 <= self.min_confidence <= 1.0:
            raise InvalidRecallQuery(
                "min_confidence must be between 0.0 and 1.0"
            )

        if self.category is None and not self.text:
            raise InvalidRecallQuery(
                "At least one filter (category or text) must be provided"
            )

        if self.limit is not None and self.limit <= 0:
            raise InvalidRecallQuery("limit must be positive")

        if not isinstance(self.match_mode, MatchMode):
            raise InvalidRecallQuery("Invalid match_mode")
