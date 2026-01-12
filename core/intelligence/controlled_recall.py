from typing import Optional, List

from core.memory.usage_mode import MemoryUsageMode
from core.memory.permit import MemoryPermit
from core.memory.guards import (
    ensure_memory_allowed,
    ensure_valid_permit,
)

from core.memory.recall.recall_query import RecallQuery
from core.memory.recall.recall_result import RecallResult
from core.memory.recall.recall_manager import MemoryRecallManager


def controlled_recall(
    *,
    system_mode: MemoryUsageMode,
    permit: Optional[MemoryPermit],
    query: RecallQuery,
) -> List[RecallResult]:
    """
    The ONLY authorized entry point for memory recall.

    Guarantees:
    - explicit opt-in
    - read-only recall
    - no intent / confidence mutation
    - safe degradation
    """

    # 1️⃣ Global memory switch
    ensure_memory_allowed(system_mode)

    # 2️⃣ Permit required
    if permit is None:
        raise PermissionError("Memory permit is required for recall")

    ensure_valid_permit(permit)

    # 3️⃣ Mode alignment
    if permit.mode != system_mode:
        raise PermissionError("Memory permit mode mismatch")

    # 4️⃣ Defensive expiry check
    if permit.is_expired():
        raise PermissionError("Memory permit has expired")

    # 5️⃣ Scoped, immutable query
    scoped_query = RecallQuery(
        text=query.text,
        match_mode=query.match_mode,
        category=query.category,
        min_confidence=max(query.min_confidence, permit.min_confidence),
        limit=permit.max_results or query.limit,
    )

    # 6️⃣ Safe recall execution
    try:
        manager = MemoryRecallManager()
        return manager.recall(scoped_query)
    except Exception:
        # 🔒 Never leak recall failures upward
        return []
