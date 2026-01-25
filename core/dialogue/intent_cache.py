# core/dialogue/intent_cache.py

import time
from typing import Optional


class IntentCache:
    """
    Day 74 — Session-local intent cache.

    - In-memory only
    - Auto-expiring
    - Deterministic
    """

    def __init__(self, ttl_sec: float = 10.0):
        self._ttl = ttl_sec
        self._intent: Optional[str] = None
        self._timestamp: float = 0.0

    def set(self, intent: str) -> None:
        self._intent = intent
        self._timestamp = time.time()

    def get(self) -> Optional[str]:
        if not self._intent:
            return None
        if (time.time() - self._timestamp) > self._ttl:
            self._intent = None
            return None
        return self._intent
