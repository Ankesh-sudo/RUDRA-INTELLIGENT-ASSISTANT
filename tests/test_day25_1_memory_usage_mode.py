import pytest

from core.memory.usage_mode import MemoryUsageMode
from core.memory.guards import ensure_memory_allowed


def test_memory_usage_mode_enum_members():
    modes = list(MemoryUsageMode)
    assert len(modes) == 4
    assert MemoryUsageMode.DISABLED in modes
    assert MemoryUsageMode.ONCE in modes
    assert MemoryUsageMode.SESSION in modes
    assert MemoryUsageMode.SCOPED in modes


def test_guard_blocks_disabled_mode():
    with pytest.raises(PermissionError):
        ensure_memory_allowed(MemoryUsageMode.DISABLED)


def test_guard_allows_non_disabled_modes():
    ensure_memory_allowed(MemoryUsageMode.ONCE)
    ensure_memory_allowed(MemoryUsageMode.SESSION)
    ensure_memory_allowed(MemoryUsageMode.SCOPED)
