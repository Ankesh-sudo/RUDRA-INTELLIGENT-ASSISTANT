from datetime import datetime

from core.memory.memory_manager import MemoryManager
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


def test_conflict_is_detected():
    manager = MemoryManager()

    existing = _entry("1", "I like dark mode", "preference")
    manager.ltm_store.save(existing)

    new = _entry("2", "I prefer dark mode", "preference")

    conflict = manager.detect_conflict(new)

    assert conflict is not None
    assert conflict.id == "1"


def test_replace_entry_replaces_old_memory():
    manager = MemoryManager()

    old = _entry("1", "I like dark mode", "preference")
    manager.ltm_store.save(old)

    new = _entry("2", "I prefer dark mode", "preference")

    conflict = manager.detect_conflict(new)
    assert conflict is not None

    manager.replace_entry(conflict, new)

    all_entries = manager.ltm_store.list_all()

    assert len(all_entries) == 1
    assert all_entries[0].id == "2"
    assert all_entries[0].content == "I prefer dark mode"


def test_reject_path_keeps_existing_memory():
    manager = MemoryManager()

    existing = _entry("1", "I like dark mode", "preference")
    manager.ltm_store.save(existing)

    new = _entry("2", "I prefer dark mode", "preference")

    conflict = manager.detect_conflict(new)
    assert conflict is not None

    # Simulate user saying "no" → do nothing

    all_entries = manager.ltm_store.list_all()

    assert len(all_entries) == 1
    assert all_entries[0].id == "1"
    assert all_entries[0].content == "I like dark mode"
