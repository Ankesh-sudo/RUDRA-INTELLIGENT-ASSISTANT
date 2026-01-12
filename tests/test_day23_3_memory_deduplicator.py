from datetime import datetime

from core.memory.deduplicator import MemoryDeduplicator
from core.memory.ltm.entry import LongTermMemoryEntry


def _entry(entry_id: str, content: str, memory_type: str):
    return LongTermMemoryEntry(
        id=entry_id,
        type=memory_type,
        content=content,
        confidence=1.0,
        source="user_confirmed",
        created_at=datetime.utcnow(),
        last_reinforced_at=None,
        explain_reason="test"
    )


def test_exact_duplicate_detection():
    deduplicator = MemoryDeduplicator()

    existing = [
        _entry("1", "I like dark mode", "preference")
    ]
    new = _entry("2", "I like dark mode", "preference")

    result = deduplicator.check(new, existing)

    assert result == "duplicate"


def test_near_duplicate_detection():
    deduplicator = MemoryDeduplicator()

    existing = [
        _entry("1", "I like dark mode", "preference")
    ]
    new = _entry("2", "I prefer dark mode", "preference")

    result = deduplicator.check(new, existing)

    assert result == "conflict_candidate"


def test_unique_memory_detection():
    deduplicator = MemoryDeduplicator()

    existing = [
        _entry("1", "I like dark mode", "preference")
    ]
    new = _entry("2", "I like light mode", "preference")

    result = deduplicator.check(new, existing)

    assert result == "unique"


def test_different_type_treated_as_unique():
    deduplicator = MemoryDeduplicator()

    existing = [
        _entry("1", "I like dark mode", "preference")
    ]
    new = _entry("2", "I like dark mode", "fact")

    result = deduplicator.check(new, existing)

    assert result == "unique"
