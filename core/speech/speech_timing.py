import time


class SpeechTiming:
    """
    Day 72 — Deterministic speech timing gate.

    Controls WHEN speech is allowed.
    Does NOT control content, voice, tone, or persona.
    """

    def __init__(self, min_delay_sec: float = 0.0):
        self._min_delay_sec = max(0.0, min_delay_sec)

    def wait(self) -> None:
        if self._min_delay_sec > 0:
            time.sleep(self._min_delay_sec)
