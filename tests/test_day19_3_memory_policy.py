"""
Day 19.3 Test — MemoryDecisionEngine (Write Gatekeeper)

Purpose:
- Validate memory write decisions
- Prevent accidental memory pollution
- Lock confidence + content rules
"""

from core.memory.memory_policy import MemoryDecisionEngine, MemoryType


def test_low_confidence_blocks_memory():
    """
    Any input below confidence threshold must not be stored.
    """
    decision = MemoryDecisionEngine.decide(
        intent_name="greeting",
        confidence=0.40,
        content_type="conversation"
    )
    assert decision == MemoryType.NONE


def test_conversation_goes_to_stm():
    """
    Conversational continuity belongs in STM.
    """
    decision = MemoryDecisionEngine.decide(
        intent_name="greeting",
        confidence=0.90,
        content_type="conversation"
    )
    assert decision == MemoryType.STM


def test_user_fact_goes_to_ltm():
    """
    Stable user facts must be persisted in LTM.
    """
    decision = MemoryDecisionEngine.decide(
        intent_name="user_fact",
        confidence=0.95,
        content_type="user_fact"
    )
    assert decision == MemoryType.LTM


def test_user_preference_goes_to_ltm():
    """
    User preferences are long-term memory.
    """
    decision = MemoryDecisionEngine.decide(
        intent_name="user_preference",
        confidence=0.85,
        content_type="user_preference"
    )
    assert decision == MemoryType.LTM


def test_command_is_never_stored():
    """
    Commands must never be written to memory.
    """
    decision = MemoryDecisionEngine.decide(
        intent_name="open_browser",
        confidence=0.99,
        content_type="command"
    )
    assert decision == MemoryType.NONE


def test_system_content_is_never_stored():
    """
    System-level messages must never be persisted.
    """
    decision = MemoryDecisionEngine.decide(
        intent_name="system_event",
        confidence=1.00,
        content_type="system"
    )
    assert decision == MemoryType.NONE
