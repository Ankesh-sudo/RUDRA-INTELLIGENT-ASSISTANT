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

    def recall(self, query: RecallQuery) -> list[RecallResult]:
        if not READ_ONLY:
            raise RecallAccessViolation("Recall layer must be read-only")

        logger.info(
            "LTM recall requested | category={} | text={} | min_confidence={}",
            query.category,
            query.text,
            query.min_confidence,
        )

        # Day 24.1 ends here — no recall logic allowed
        raise NotImplementedError(
            "Recall logic not implemented (Day 24.1 skeleton)"
        )
