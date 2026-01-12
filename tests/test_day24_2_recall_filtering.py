from datetime import datetime, timedelta
from unittest.mock import patch

from core.memory.recall import MemoryRecallManager, RecallQuery
from core.memory.types import MemoryCategory


# ----------------------------
# Fake LTM Entry (read-only)
# ----------------------------
class FakeLTMEntry:
    def __init__(
        self,
        id,
        category,
        content,
        confidence,
        created_at,
        last_updated,
    ):
        self.id = id
        self.category = category
        self.content = content
        self.confidence = confidence
        self.created_at = created_at
        self.last_updated = last_updated


# ----------------------------
# Test Data Factory
# ----------------------------
def make_entries():
    now = datetime.utcnow()

    return [
        FakeLTMEntry(
            id="1",
            category=MemoryCategory.FACT,
            content="Laptop has 16GB RAM",
            confidence=0.9,
            created_at=now - timedelta(days=10),
            last_updated=now - timedelta(days=1),
        ),
        FakeLTMEntry(
            id="2",
            category=MemoryCategory.PREFERENCE,
            content="Prefers dark theme",
            confidence=0.95,
            created_at=now - timedelta(days=5),
            last_updated=now - timedelta(days=2),
        ),
        FakeLTMEntry(
            id="3",
            category=MemoryCategory.FACT,
            content="Uses Ubuntu Linux",
            confidence=0.7,
            created_at=now - timedelta(days=20),
            last_updated=now - timedelta(days=15),
        ),
        FakeLTMEntry(
            id="4",
            category=MemoryCategory.FACT,
            content="Has RTX 3050 GPU",
            confidence=0.95,
            created_at=now - timedelta(days=3),
            last_updated=now - timedelta(hours=5),
        ),
    ]


# ----------------------------
# Tests
# ----------------------------

@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_filter_by_category(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(category=MemoryCategory.FACT)

    results = manager.recall(query)

    assert len(results) == 3
    assert all(r.category == MemoryCategory.FACT for r in results)


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_filter_by_min_confidence(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(category=MemoryCategory.FACT, min_confidence=0.9)

    results = manager.recall(query)

    assert len(results) == 2
    assert all(r.confidence >= 0.9 for r in results)


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_combined_filtering(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.PREFERENCE,
        min_confidence=0.9,
    )

    results = manager.recall(query)

    assert len(results) == 1
    assert results[0].content == "Prefers dark theme"


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_deterministic_ordering(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(category=MemoryCategory.FACT)

    results = manager.recall(query)

    assert results[0].content == "Has RTX 3050 GPU"
    assert results[0].confidence >= results[1].confidence


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_limit_is_respected(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.FACT,
        limit=1,
    )

    results = manager.recall(query)

    assert len(results) == 1


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_empty_result_safe(mock_fetch):
    mock_fetch.return_value = []

    manager = MemoryRecallManager()
    query = RecallQuery(category=MemoryCategory.FACT)

    results = manager.recall(query)

    assert results == []
