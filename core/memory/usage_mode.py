from enum import Enum, auto


class MemoryUsageMode(Enum):
    """
    Explicit contract describing if and how memory may be used.

    IMPORTANT:
    - This enum carries NO logic.
    - Default behavior elsewhere must remain DISABLED.
    """

    DISABLED = auto()   # Memory is completely invisible
    ONCE = auto()       # One-turn explicit permission
    SESSION = auto()    # Valid for current session only
    SCOPED = auto()     # Restricted by explicit scope (category/confidence/etc.)
