"""
Day 17.1 — Clarification Pool Tests

Purpose:
- Ensure clarification messages exist
- Ensure rotation works
- Ensure initial state is correct
"""

from core.assistant import Assistant, CLARIFICATION_MESSAGES


def test_clarification_pool_exists():
    """Clarification message pool must exist and be non-empty."""
    assert isinstance(CLARIFICATION_MESSAGES, list)
    assert len(CLARIFICATION_MESSAGES) >= 3


def test_clarification_rotation_cycles():
    """
    next_clarification() should rotate messages
    and wrap around correctly.
    """
    assistant = Assistant()

    outputs = []
    for _ in range(len(CLARIFICATION_MESSAGES) + 1):
        outputs.append(assistant.next_clarification())

    # First message should repeat after full cycle
    assert outputs[0] == outputs[-1]


def test_clarification_index_advances():
    """clarify_index should advance after each call."""
    assistant = Assistant()

    start_index = assistant.clarify_index
    assistant.next_clarification()
    assert assistant.clarify_index == (start_index + 1) % len(CLARIFICATION_MESSAGES)


def test_initial_clarification_state():
    """Initial clarification-related state must be clean."""
    assistant = Assistant()

    assert assistant.clarify_index == 0
    assert assistant.failure_count == 0
    assert assistant.last_was_clarification is False
