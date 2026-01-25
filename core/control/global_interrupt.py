from enum import Enum, auto


class GlobalInterrupt(Enum):
    """
    Global interrupt states.

    PURE ENUM.
    No controller imports.
    No logic.
    """

    IGNORE = auto()    # normal execution
    SOFT = auto()      # pause
    RESTART = auto()   # restart from beginning
    HARD = auto()      # immediate stop
