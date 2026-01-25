from core.control.interrupt_controller import InterruptController
from core.control.global_interrupt import GlobalInterrupt


class GoogleSpeechEngine:
    """
    Speech-to-text engine.

    Day 71+ rules:
    - Uses InterruptController instance
    - No global interrupt access
    - Read-only interrupt checks
    """

    def __init__(self, interrupt_controller: InterruptController):
        self._interrupts = interrupt_controller

    def listen(self) -> str | None:
        """
        Blocking listen loop.
        Returns None if interrupted.
        """

        # HARD interrupt blocks listening
        if self._interrupts.current() == GlobalInterrupt.HARD:
            return None

        # --- existing STT logic below ---
        # (unchanged, placeholder here)
        try:
            text = self._capture_audio_and_transcribe()
            return text
        except Exception:
            return None

    def _capture_audio_and_transcribe(self) -> str:
        """
        Existing Google STT logic lives here.
        """
        return ""
