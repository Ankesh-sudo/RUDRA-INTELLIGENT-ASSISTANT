from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class MemoryType(Enum):
    FACT = "fact"
    PREFERENCE = "preference"
    HABIT = "habit"

@dataclass
class LongTermMemoryEntry:
    id: str
    type: MemoryType
    content: str
    confidence: float
    source: str
    created_at: datetime
    last_reinforced_at: datetime | None
    explain_reason: str
