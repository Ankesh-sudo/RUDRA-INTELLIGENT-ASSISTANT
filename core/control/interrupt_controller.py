from threading import Event
from core.control.global_interrupt import GlobalInterrupt


class InterruptController:
    """
    Central interrupt state controller.

    Day 71 compatible:
    - HARD / SOFT / RESTART / IGNORE
    - Thread-safe
    - No execution authority
    """

    def __init__(self):
        self._interrupt_event = Event()
        self._current_interrupt: GlobalInterrupt = GlobalInterrupt.IGNORE

    # -------------------------
    # Trigger methods
    # -------------------------

    def trigger_hard(self) -> None:
        self._current_interrupt = GlobalInterrupt.HARD
        self._interrupt_event.set()

    def trigger_soft(self) -> None:
        self._current_interrupt = GlobalInterrupt.SOFT
        self._interrupt_event.set()

    def trigger_restart(self) -> None:
        self._current_interrupt = GlobalInterrupt.RESTART
        self._interrupt_event.set()

    # -------------------------
    # Clear / resume
    # -------------------------

    def clear(self) -> None:
        self._current_interrupt = GlobalInterrupt.IGNORE
        self._interrupt_event.clear()

    def clear_restart(self) -> None:
        if self._current_interrupt == GlobalInterrupt.RESTART:
            self._current_interrupt = GlobalInterrupt.IGNORE
            self._interrupt_event.clear()

    # -------------------------
    # Read-only access
    # -------------------------

    def current(self) -> GlobalInterrupt:
        return self._current_interrupt

    def is_triggered(self) -> bool:
        return self._interrupt_event.is_set()
