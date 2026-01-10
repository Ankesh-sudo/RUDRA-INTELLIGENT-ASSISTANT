"""
Short-Term Memory (STM)

Purpose:
- Store recent conversational continuity
- Limited size
- Fast recall
- Automatic decay (TTL)
"""

import time
from collections import deque


class ShortTermMemory:
    # ===============================
    # DAY 21.3 — STM LIMITS (LOCKED)
    # ===============================
    MAX_ITEMS = 50          # hard cap
    TTL_SECONDS = 300       # 5 minutes

    def __init__(self):
        # deque preserves insertion order (FIFO)
        self._items = deque()

    # -------------------------------
    # Internal helpers
    # -------------------------------
    def _now(self) -> float:
        return time.time()

    def _cleanup(self):
        """
        Remove expired or excess entries.
        """
        now = self._now()

        # TTL-based eviction
        while self._items and (now - self._items[0]["timestamp"] > self.TTL_SECONDS):
            self._items.popleft()

        # Capacity-based eviction (FIFO)
        while len(self._items) > self.MAX_ITEMS:
            self._items.popleft()

    # -------------------------------
    # Public API
    # -------------------------------
    def store(self, *, role: str, content: str, intent: str, confidence: float):
        """
        Store a short-term memory entry (in-memory only).
        """
        self._items.append({
            "role": role,
            "content": content,
            "intent": intent,
            "confidence": confidence,
            "timestamp": self._now(),
        })

        # Enforce limits immediately
        self._cleanup()

    def fetch_recent(self, limit: int = 10):
        """
        Fetch most recent STM entries (newest last).
        """
        self._cleanup()
        if limit <= 0:
            return []

        return list(self._items)[-limit:]

    def clear(self):
        """
        Clear all STM entries.
        """
        self._items.clear()
