import pytest

from core.memory.recall import (
    RecallQuery,
    MatchMode,
    MemoryRecallManager,
    InvalidRecallQuery,
)
from core.memory.types import MemoryCategory


def test_valid_recall_query_creation():
    q = RecallQuery(
        category=MemoryCategory.FACT,
        min_confidence=0.5,
        match_mode=MatchMode.CONTAINS,
    )
    assert q.min_confidence == 0.5


def test_invalid_confidence_raises():
    with pytest.raises(InvalidRecallQuery):
        RecallQuery(
            category=MemoryCategory.FACT,
            min_confidence=1.5,
        )


def test_query_requires_filter():
    with pytest.raises(InvalidRecallQuery):
        RecallQuery()


def test_recall_method_exists_and_raises_not_implemented():
    manager = MemoryRecallManager()
    query = RecallQuery(category=MemoryCategory.FACT)

    with pytest.raises(NotImplementedError):
        manager.recall(query)
