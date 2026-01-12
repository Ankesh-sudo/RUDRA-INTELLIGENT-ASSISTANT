from typing import List

from core.memory.trace import MemoryUsageTrace


class MemoryTraceSink:
    """
    Ephemeral sink for memory usage traces.

    - NOT persisted
    - NOT long-term
    - Cleared on session end
    """

    def __init__(self):
        self._traces: List[MemoryUsageTrace] = []

    def record(self, trace: MemoryUsageTrace) -> None:
        self._traces.append(trace)

    def fetch_all(self) -> list[MemoryUsageTrace]:
        return list(self._traces)

    def clear(self) -> None:
        self._traces.clear()
