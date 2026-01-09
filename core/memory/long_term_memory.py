"""
Long-Term Memory (LTM)

Purpose:
- Store stable user information
- Preferences, facts
"""

class LongTermMemory:
    def store(self, *, content: str, memory_type: str, confidence: float):
        """
        Store a long-term memory entry.
        DB write will be added later.
        """
        # skeleton — no-op
        return

    def fetch_by_type(self, memory_type: str):
        return []
