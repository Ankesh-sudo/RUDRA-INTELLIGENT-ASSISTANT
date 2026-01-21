from enum import Enum, auto


class SessionState(Enum):
    """
    Lifecycle of a single execution session.
    """
    CREATED = auto()
    PLANNED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class StepState(Enum):
    """
    Lifecycle of a single planned step.
    """
    PENDING = auto()
    READY = auto()
    RUNNING = auto()
    DONE = auto()
    FAILED = auto()
    SKIPPED = auto()
