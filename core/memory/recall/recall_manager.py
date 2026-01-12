from loguru import logger

from .recall_query import RecallQuery, MatchMode
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

    def _normalize(self, text: str) -> str:
        """
        Deterministic normalization for recall comparison only.
        """
        return text.strip().lower()

    def recall(self, query: RecallQuery) -> list[RecallResult]:
        if not READ_ONLY:
            raise RecallAccessViolation("Recall layer must be read-only")

        logger.info(
            "LTM recall requested | category={} | text={} | min_confidence={} | match_mode={}",
            query.category,
            query.text,
            query.min_confidence,
            query.match_mode,
        )

        # 1️⃣ Fetch all entries (read-only)
        entries = self._fetch_all_ltm_entries()

        # 2️⃣ Deterministic filtering
        filtered = []
        for entry in entries:
            # Category filter
            if query.category and entry.category != query.category:
                continue

            # Confidence filter
            if entry.confidence < query.min_confidence:
                continue

            # Text matching filter
            if query.text:
                entry_text = self._normalize(entry.content)
                query_text = self._normalize(query.text)

                if query.match_mode == MatchMode.EXACT:
                    if entry_text != query_text:
                        continue

                elif query.match_mode == MatchMode.CONTAINS:
                    if query_text not in entry_text:
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

        # 5️⃣ Map to RecallResult
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
