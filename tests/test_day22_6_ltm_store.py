from datetime import datetime

from core.memory.ltm.in_memory_store import InMemoryLongTermMemoryStore
from core.memory.ltm.entry import LongTermMemoryEntry


def test_ltm_store_save_and_list():
    store = InMemoryLongTermMemoryStore()

    entry = LongTermMemoryEntry(
        id="test-id-1",
        type=None,
        content="User prefers Chrome browser",
        confidence=0.9,
        source="user_confirmed",
        created_at=datetime.utcnow(),
        last_reinforced_at=None,
        explain_reason="Approved by user"
    )

    store.save(entry)

    entries = store.list_all()

    assert len(entries) == 1
    assert entries[0].id == "test-id-1"
    assert entries[0].content == "User prefers Chrome browser"
    assert entries[0].confidence == 0.9
    assert entries[0].source == "user_confirmed"


def test_ltm_store_delete():
    store = InMemoryLongTermMemoryStore()

    entry1 = LongTermMemoryEntry(
        id="1",
        type=None,
        content="Memory one",
        confidence=0.8,
        source="user_confirmed",
        created_at=datetime.utcnow(),
        last_reinforced_at=None,
        explain_reason="Test"
    )

    entry2 = LongTermMemoryEntry(
        id="2",
        type=None,
        content="Memory two",
        confidence=0.7,
        source="user_confirmed",
        created_at=datetime.utcnow(),
        last_reinforced_at=None,
        explain_reason="Test"
    )

    store.save(entry1)
    store.save(entry2)

    store.delete("1")
    entries = store.list_all()

    assert len(entries) == 1
    assert entries[0].id == "2"


def test_ltm_store_clear():
    store = InMemoryLongTermMemoryStore()

    entry = LongTermMemoryEntry(
        id="clear-test",
        type=None,
        content="Temporary memory",
        confidence=0.5,
        source="user_confirmed",
        created_at=datetime.utcnow(),
        last_reinforced_at=None,
        explain_reason="Test clear"
    )

    store.save(entry)
    assert len(store.list_all()) == 1

    store.clear()
    assert store.list_all() == []
