from typing import List
from core.memory.ltm.entry import LongTermMemoryEntry


class InMemoryLongTermMemoryStore:
    """
    Temporary in-memory Long-Term Memory store.

    Characteristics:
    - No persistence across runs
    - No indexing or optimization
    - Fully inspectable
    - Safe for early LTM activation
    """

    def __init__(self):
        self._entries: List[LongTermMemoryEntry] = []

    def save(self, entry: LongTermMemoryEntry) -> None:
        """
        Store a long-term memory entry.
        """
        self._entries.append(entry)

    def list_all(self) -> List[LongTermMemoryEntry]:
        """
        Return all stored LTM entries.
        """
        return list(self._entries)

    def delete(self, entry_id: str) -> None:
        """
        Delete a memory entry by ID.
        """
        self._entries = [
            entry for entry in self._entries
            if entry.id != entry_id
        ]

    def clear(self) -> None:
        """
        Remove all stored memories (useful for tests).
        """
        self._entries.clear()
