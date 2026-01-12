from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

from core.memory.usage_mode import MemoryUsageMode


@dataclass(frozen=True)
class MemoryPermit:
    """
    Explicit, immutable authorization token for memory usage.

    A permit must be passed intentionally into any component
    that wishes to use recall.
    """

    mode: MemoryUsageMode

    allowed_categories: Optional[Iterable[str]] = None
    min_confidence: float = 0.0
    max_results: Optional[int] = None

    issued_at: datetime = datetime.utcnow()
    expires_at: Optional[datetime] = None

    issued_by: str = "user"  # user | system (future-safe)

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
