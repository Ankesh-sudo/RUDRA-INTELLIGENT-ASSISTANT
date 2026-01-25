import time
from loguru import logger

from core.speech.google_engine import GoogleSpeechEngine
from core.speech.wake_word import contains_wake_word
from core.control.interrupt_controller import InterruptController
from core.control.global_interrupt import GlobalInterrupt


class InputController:
    """
    Handles microphone input and wake-word logic.

    Day 71+ rules:
    - No global interrupt access
    - Uses injected InterruptController
    - No memory or persona access
    """

    ACTIVE_TIMEOUT = 45  # seconds

    def __init__(self, interrupt_controller: InterruptController):
        self._interrupts = interrupt_controller
        self.speech = GoogleSpeechEngine(self._interrupts)

        self.active = False
        self.last_active_time = 0.0

    def reset_execution_state(self) -> None:
        """
        Reset ONLY execution-related state.
        Memory, learning, and dialogue context remain untouched.
        """
        logger.warning("Execution state reset due to HARD interrupt")
        self.active = False
        self.last_active_time = 0.0

    def read(self) -> str:
        """
        Blocking input read.
        Returns empty string if interrupted or inactive.
        """

        # 🔴 Abort immediately if HARD interrupt already active
        if self._interrupts.current() == GlobalInterrupt.HARD:
            logger.debug("Input read aborted due to HARD interrupt")
            return ""

        # Ask for ENTER only when sleeping
        if not self.active:
            input("Press ENTER and speak...")

        # --- Primary path: Speech ---
        text = self.speech.listen()
        logger.debug("Raw speech: {}", text)

        # 🔁 FALLBACK: Keyboard input (temporary, safe)
        if not text:
            text = input("You (keyboard fallback) > ").strip()

        # Interrupt may occur during listening
        if self._interrupts.current() == GlobalInterrupt.HARD:
            logger.debug("HARD interrupt triggered after listening")
            self.reset_execution_state()
            return ""

        if not text:
            return ""

        now = time.time()

        # If already active, accept speech directly
        if self.active and (now - self.last_active_time) < self.ACTIVE_TIMEOUT:
            self.last_active_time = now
            return text

        # Wake-word detection
        if contains_wake_word(text):
            self.active = True
            self.last_active_time = now

            clean_text = (
                text.lower()
                .replace("rudra", "")
                .strip()
            )

            if not clean_text:
                print("Rudra > Yes?")
                return ""

            return clean_text

        # No wake word and not active
        print("Rudra > (going to sleep)")
        self.active = False
        return ""
