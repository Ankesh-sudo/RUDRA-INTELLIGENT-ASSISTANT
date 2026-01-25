# core/dialogue/session_dialogue_state.py

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SessionDialogueState:
    """
    Day 73 — Session-level dialogue context.

    Rules:
    - In-memory only
    - No persistence
    - No persona access
    - Auto-expiring
    """

    topic: Optional[str] = None
    last_intent: Optional[str] = None
    last_updated: float = field(default_factory=time.time)
    ttl_sec: float = 120.0  # default context lifetime

    def update(self, *, topic: Optional[str], intent: Optional[str]) -> None:
        self.topic = topic or self.topic
        self.last_intent = intent or self.last_intent
        self.last_updated = time.time()

    def is_expired(self) -> bool:
        return (time.time() - self.last_updated) > self.ttl_sec

    def reset_if_expired(self) -> None:
        if self.is_expired():
            self.topic = None
            self.last_intent = None
            self.last_updated = time.time()
