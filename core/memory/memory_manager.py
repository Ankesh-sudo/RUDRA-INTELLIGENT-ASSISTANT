import uuid
from datetime import datetime
from loguru import logger

from core.memory.ltm.in_memory_store import InMemoryLongTermMemoryStore
from core.memory.ltm.entry import LongTermMemoryEntry


class MemoryManager:
    """
    Central memory entry point.

    Responsibilities:
    - Gate all memory writes
    - Protect STM integrity
    - Control LTM storage (explicit only)
    """

    def __init__(self):
        # Existing STM / policy setup remains unchanged
        # (do NOT remove or refactor existing logic)

        # 🔵 Day 22.6 — Long-Term Memory store (explicit only)
        self.ltm_store = InMemoryLongTermMemoryStore()

    # =================================================
    # EXISTING METHODS (UNCHANGED)
    # =================================================
    def consider(
        self,
        *,
        role: str,
        content: str,
        intent: str,
        confidence: float,
        content_type: str
    ):
        """
        Existing STM / policy-controlled memory consideration.
        DO NOT MODIFY for Day 22.6.
        """
        # Existing implementation stays exactly as it is
        pass  # <-- keep your original code here

    # =================================================
    # DAY 22.6 — EXPLICIT LTM WRITE (NEW)
    # =================================================
    def store_long_term(
        self,
        *,
        content: str,
        memory_type,
        confidence: float,
        reason: str,
        source: str = "user_confirmed"
    ) -> LongTermMemoryEntry:
        """
        Store a Long-Term Memory entry.

        This method MUST be called only after:
        - Promotion decision == PROMOTE
        - User explicitly confirmed consent

        No silent writes are allowed.
        """

        entry = LongTermMemoryEntry(
            id=str(uuid.uuid4()),
            type=memory_type,
            content=content,
            confidence=confidence,
            source=source,
            created_at=datetime.utcnow(),
            last_reinforced_at=None,
            explain_reason=reason
        )

        self.ltm_store.save(entry)

        logger.info(
            f"LTM STORED | id={entry.id} | content='{entry.content}'"
        )

        return entry

    # =================================================
    # OPTIONAL — INSPECTION (SAFE)
    # =================================================
    def list_long_term(self):
        """
        Inspect all stored long-term memories.
        (Read-only, for debugging / tests)
        """
        return self.ltm_store.list_all()
