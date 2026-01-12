from datetime import datetime, timedelta
from unittest.mock import patch

from core.memory.recall import MemoryRecallManager, RecallQuery, MatchMode
from core.memory.types import MemoryCategory


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
            category=MemoryCategory.FACT,
            content="Uses Ubuntu Linux",
            confidence=0.8,
            created_at=now - timedelta(days=5),
            last_updated=now - timedelta(days=2),
        ),
    ]


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_exact_match_success(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.FACT,
        text="laptop has 16gb ram",
        match_mode=MatchMode.EXACT,
    )

    results = manager.recall(query)

    assert len(results) == 1
    assert results[0].content == "Laptop has 16GB RAM"


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_exact_match_failure(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.FACT,
        text="Laptop RAM",
        match_mode=MatchMode.EXACT,
    )

    results = manager.recall(query)

    assert results == []


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_contains_match_success(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.FACT,
        text="ubuntu",
        match_mode=MatchMode.CONTAINS,
    )

    results = manager.recall(query)

    assert len(results) == 1
    assert "Ubuntu" in results[0].content


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_contains_match_case_insensitive(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.FACT,
        text="UBUNTU",
        match_mode=MatchMode.CONTAINS,
    )

    results = manager.recall(query)

    assert len(results) == 1


@patch.object(MemoryRecallManager, "_fetch_all_ltm_entries")
def test_text_filter_combined_with_confidence(mock_fetch):
    mock_fetch.return_value = make_entries()

    manager = MemoryRecallManager()
    query = RecallQuery(
        category=MemoryCategory.FACT,
        text="ubuntu",
        match_mode=MatchMode.CONTAINS,
        min_confidence=0.85,
    )

    results = manager.recall(query)

    assert results == []
