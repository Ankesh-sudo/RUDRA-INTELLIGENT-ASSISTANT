from enum import Enum, auto


class GlobalInterruptState(Enum):
    """
    Global interrupt states.
    """
    IGNORE = auto()
    SOFT = auto()
    RESTART = auto()
    HARD = auto()


# Backward compatibility alias
GlobalInterrupt = GlobalInterruptState


class GlobalInterruptController:
    """
    Global interrupt controller (singleton).
    """

    def __init__(self):
        self.state = GlobalInterruptState.IGNORE

    def trigger(self, state: GlobalInterruptState = GlobalInterruptState.HARD):
        self.state = state

    def clear(self):
        self.state = GlobalInterruptState.IGNORE

    def is_active(self) -> bool:
        return self.state != GlobalInterruptState.IGNORE

    # 🔧 COMPATIBILITY METHOD (REQUIRED)
    def current(self) -> GlobalInterruptState:
        return self.state


# Singleton instance
GLOBAL_INTERRUPT = GlobalInterruptController()
