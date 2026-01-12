from loguru import logger

from .recall_query import RecallQuery
from .recall_result import RecallResult
from .exceptions import RecallAccessViolation

# HARD GUARANTEE
READ_ONLY = True


class MemoryRecallManager:
    """
    Read-only memory recall boundary.
    No writes, no mutation, no inference.
    """

    def _fetch_all_ltm_entries(self):
        """
        Read-only fetch of all LTM entries.
        No filtering. No mutation.
        """
        from core.memory.long_term_memory import LongTermMemory

        return LongTermMemory.get_all_entries()

    def recall(self, query: RecallQuery) -> list[RecallResult]:
        if not READ_ONLY:
            raise RecallAccessViolation("Recall layer must be read-only")

        logger.info(
            "LTM recall requested | category={} | text={} | min_confidence={}",
            query.category,
            query.text,
            query.min_confidence,
        )

        # 1️⃣ Fetch all LTM entries (read-only)
        entries = self._fetch_all_ltm_entries()

        # 2️⃣ Deterministic filtering
        filtered = []
        for entry in entries:
            if query.category and entry.category != query.category:
                continue

            if entry.confidence < query.min_confidence:
                continue

            filtered.append(entry)

        # 3️⃣ Deterministic ordering (confidence ↓, last_updated ↓)
        filtered.sort(
            key=lambda e: (e.confidence, e.last_updated),
            reverse=True,
        )

        # 4️⃣ Apply limit (after sorting)
        if query.limit:
            filtered = filtered[: query.limit]

        # 5️⃣ Map to RecallResult (pure projection)
        return [
            RecallResult(
                memory_id=entry.id,
                category=entry.category,
                content=entry.content,
                confidence=entry.confidence,
                created_at=entry.created_at,
                last_updated=entry.last_updated,
            )
            for entry in filtered
        ]
