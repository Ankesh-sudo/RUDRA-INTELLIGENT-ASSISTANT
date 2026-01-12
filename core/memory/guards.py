from core.memory.usage_mode import MemoryUsageMode
from core.memory.permit import MemoryPermit


def ensure_memory_allowed(mode: MemoryUsageMode) -> None:
    """
    Hard guardrail enforcing explicit memory permission.

    This guard blocks ALL memory usage when the system
    is in DISABLED mode.

    Wired at the single recall injection point (Day 25.3).
    """
    if mode == MemoryUsageMode.DISABLED:
        raise PermissionError("Memory usage is disabled by default")


def ensure_valid_permit(permit: MemoryPermit) -> None:
    """
    Enforces permit-level validity before memory usage.

    A valid permit must:
    - Exist
    - Not be expired

    No scope or mode enforcement happens here.
    That is handled at the recall boundary.
    """
    if permit.is_expired():
        raise PermissionError("Memory permit has expired")
