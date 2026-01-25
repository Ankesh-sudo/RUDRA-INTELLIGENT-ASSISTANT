from loguru import logger

from core.input.input_validator import InputValidator
from core.input_controller import InputController

from core.control.interrupt_controller import InterruptController
from core.control.global_interrupt import GlobalInterrupt

from core.actions.action_executor import ActionExecutor


IDLE = "idle"


class Assistant:
    """
    Assistant — Compatibility Mode (Day 75)

    PURPOSE:
    - Allow Rudra to run safely right now
    - No global interrupt usage
    - No memory writes
    - No persona authority
    - No dialogue engine coupling yet

    This WILL be refactored properly in Day 76–79.
    """

    def __init__(self):
        # -------------------------------------------------
        # 🔐 SINGLE INTERRUPT AUTHORITY
        # -------------------------------------------------
        self.interrupts = InterruptController()

        # -------------------------------------------------
        # 🎤 INPUT
        # -------------------------------------------------
        self.input = InputController(self.interrupts)
        self.input_validator = InputValidator()

        # -------------------------------------------------
        # ⚙️ EXECUTION (SAFE, LIMITED)
        # -------------------------------------------------
        self.action_executor = ActionExecutor()

        # -------------------------------------------------
        # STATE
        # -------------------------------------------------
        self.running = True
        self.state = IDLE

    # =================================================
    # CORE LOOP (SAFE MODE)
    # =================================================
    def _cycle(self) -> None:
        # Abort immediately on HARD interrupt
        if self.interrupts.current() == GlobalInterrupt.HARD:
            logger.warning("HARD interrupt detected — resetting execution state")
            self.input.reset_execution_state()
            return

        raw_text = self.input.read()
        if not raw_text:
            return

        validation = self.input_validator.validate(raw_text)
        if not validation["valid"]:
            print("Rudra > Please repeat.")
            return

        clean_text = validation["clean_text"]

        # -------------------------------------------------
        # TEMPORARY BEHAVIOR (DAY 75)
        # -------------------------------------------------
        # No intent resolution
        # No memory writes
        # No persona routing
        # Just confirm input path is alive
        # -------------------------------------------------
        print(f"Rudra > I heard: {clean_text}")

    # =================================================
    # RUN LOOPS
    # =================================================
    def run(self) -> None:
        logger.info("Rudra started (Day 75 compatibility mode)")
        while self.running:
            self._cycle()

    def run_once(self) -> None:
        self._cycle()
