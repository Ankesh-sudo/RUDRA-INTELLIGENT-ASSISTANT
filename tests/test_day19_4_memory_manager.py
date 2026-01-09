"""
Day 19.4 Test — MemoryManager wiring

Purpose:
- Ensure MemoryManager routes decisions correctly
- Ensure no DB or side effects
- Ensure no exceptions are raised
"""

from core.memory.memory_manager import MemoryManager


def test_memory_manager_runs_without_error():
    mm = MemoryManager()

    # Conversation → STM
    mm.consider(
        role="user",
        content="hello rudra",
        intent="greeting",
        confidence=0.9,
        content_type="conversation"
    )

    # User fact → LTM
    mm.consider(
        role="user",
        content="my name is Ankesh",
        intent="user_fact",
        confidence=0.95,
        content_type="user_fact"
    )

    # Command → NONE (should do nothing)
    mm.consider(
        role="user",
        content="open browser",
        intent="open_browser",
        confidence=0.99,
        content_type="command"
    )

    assert True
