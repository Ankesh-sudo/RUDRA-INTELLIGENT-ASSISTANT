from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

from core.memory.usage_mode import MemoryUsageMode


@dataclass(frozen=True)
class MemoryUsageTrace:
    """
    Immutable audit record for a single memory usage event.
    """

    permit_mode: MemoryUsageMode
    query_text: Optional[str]
    query_category: Optional[str]

    result_ids: Iterable[int]

    timestamp: datetime
    consumer: str  # e.g. "intelligence", "skill", "ui"
