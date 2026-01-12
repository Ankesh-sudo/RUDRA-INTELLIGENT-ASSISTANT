import pytest
from datetime import datetime, timedelta

from core.intelligence.controlled_recall import controlled_recall
from core.memory.usage_mode import MemoryUsageMode
from core.memory.permit import MemoryPermit
from core.memory.recall.recall_query import RecallQuery, MatchMode


def test_recall_blocked_without_permit():
    query = RecallQuery(text="test", match_mode=MatchMode.EXACT)

    with pytest.raises(PermissionError):
        controlled_recall(
            system_mode=MemoryUsageMode.ONCE,
            permit=None,
            query=query,
        )


def test_recall_blocked_when_disabled():
    permit = MemoryPermit(mode=MemoryUsageMode.ONCE)
    query = RecallQuery(text="test", match_mode=MatchMode.EXACT)

    with pytest.raises(PermissionError):
        controlled_recall(
            system_mode=MemoryUsageMode.DISABLED,
            permit=permit,
            query=query,
        )


def test_expired_permit_blocks_recall():
    expired = MemoryPermit(
        mode=MemoryUsageMode.ONCE,
        expires_at=datetime.utcnow() - timedelta(seconds=1),
    )
    query = RecallQuery(text="test", match_mode=MatchMode.EXACT)

    with pytest.raises(PermissionError):
        controlled_recall(
            system_mode=MemoryUsageMode.ONCE,
            permit=expired,
            query=query,
        )
