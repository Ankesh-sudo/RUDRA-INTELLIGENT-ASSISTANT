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
    - Day 23.1 compliant (schema-ready, behavior-unchanged)
    """

    def __init__(self):
        self._entries: List[LongTermMemoryEntry] = []

    def save(self, entry: LongTermMemoryEntry) -> None:
        """
        Store a LongTermMemoryEntry exactly as provided.

        IMPORTANT:
        - No mutation
        - No inference
        - No schema enforcement here
        - Entry evolution happens in Day 23.2+
        """
        self._entries.append(entry)

    def list_all(self) -> List[LongTermMemoryEntry]:
        """
        Return all stored LTM entries.
        """
        return list(self._entries)

    def delete(self, entry_id: str) -> bool:
        """
        Delete a memory entry by ID.

        Returns:
            True if deletion occurred, False otherwise
        """
        before = len(self._entries)
        self._entries = [
            entry for entry in self._entries
            if entry.id != entry_id
        ]
        return len(self._entries) < before

    def clear(self) -> None:
        """
        Remove all stored memories (useful for tests).
        """
        self._entries.clear()
