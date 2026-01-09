"""
Day 20.1 Test — Context Pack Builder (Read-Only)

Purpose:
- Ensure ContextPackBuilder builds a valid context pack
- Ensure structure is stable and predictable
- No DB, no side effects
"""

from core.memory.context_pack import ContextPackBuilder


def test_context_pack_builds_cleanly():
    builder = ContextPackBuilder()
    pack = builder.build()

    # Must be a dict
    assert isinstance(pack, dict)

    # Required keys
    assert "recent_conversation" in pack
    assert "user_facts" in pack
    assert "user_preferences" in pack

    # Values must be lists (even if empty)
    assert isinstance(pack["recent_conversation"], list)
    assert isinstance(pack["user_facts"], list)
    assert isinstance(pack["user_preferences"], list)
