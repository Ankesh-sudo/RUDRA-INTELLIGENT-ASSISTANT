from dataclasses import dataclass
from datetime import datetime

from core.memory.types import MemoryCategory


@dataclass(frozen=True)
class RecallResult:
    memory_id: str
    category: MemoryCategory
    content: str
    confidence: float
    created_at: datetime
    last_updated: datetime
