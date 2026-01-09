"""
Short-Term Memory (STM)

Purpose:
- Store recent conversational continuity
- Limited size
- Fast recall
"""

class ShortTermMemory:
    def store(self, *, role: str, content: str, intent: str, confidence: float):
        """
        Store a short-term memory entry.
        DB write will be added later.
        """
        # skeleton — no-op
        return

    def fetch_recent(self, limit: int = 10):
        """
        Fetch recent STM entries.
        """
        return []
