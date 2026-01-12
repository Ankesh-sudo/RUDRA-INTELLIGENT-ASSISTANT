from core.memory.usage_mode import MemoryUsageMode


def ensure_memory_allowed(mode: MemoryUsageMode) -> None:
    """
    Hard guardrail enforcing explicit memory permission.

    This function MUST be called at the single recall injection point
    (wired in Day 25.3).

    Raises:
        PermissionError: if memory usage is disabled
    """
    if mode == MemoryUsageMode.DISABLED:
        raise PermissionError("Memory usage is disabled by default")
