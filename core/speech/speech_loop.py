# core/speech/speech_loop.py

import time
from typing import Callable

from core.control.interrupt_controller import InterruptController
from core.control.global_interrupt import GlobalInterrupt


class SpeechLoop:
    """
    Day 71: Interruptible Speech Loop

    Responsibilities:
    - Speak text in a controlled loop
    - Honor PAUSE / RESUME / RESTART
    - NO memory writes
    - NO persona logic
    - NO execution side effects
    """

    def __init__(
        self,
        speak_fn: Callable[[str], None],
        interrupt_controller: InterruptController,
    ):
        self._speak_fn = speak_fn
        self._interrupts = interrupt_controller

    def speak(self, text: str) -> None:
        """
        Blocking, interrupt-aware speech loop.
        """
        self._interrupts.clear_restart()

        while True:
            interrupt = self._interrupts.current()

            if interrupt == GlobalInterrupt.HARD:
                return  # immediate stop

            if interrupt == GlobalInterrupt.RESTART:
                self._interrupts.clear_restart()
                continue  # restart from beginning

            if interrupt == GlobalInterrupt.SOFT:
                self._wait_until_resumed()
                continue

            # Safe to speak
            self._speak_fn(text)
            return

    def _wait_until_resumed(self) -> None:
        """
        Pause loop until interrupt clears.
        """
        while True:
            interrupt = self._interrupts.current()

            if interrupt == GlobalInterrupt.HARD:
                return

            if interrupt == GlobalInterrupt.RESTART:
                self._interrupts.clear_restart()
                return

            if interrupt == GlobalInterrupt.IGNORE:
                return

            time.sleep(0.05)
