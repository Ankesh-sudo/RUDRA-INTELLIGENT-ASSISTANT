# core/dialogue/silence_detector.py

import time


class SilenceDetector:
    """
    Day 73 — Silence detection.

    Determines whether enough time has passed
    to consider the conversation paused/reset.
    """

    def __init__(self, silence_threshold_sec: float = 5.0):
        self._threshold = max(0.0, silence_threshold_sec)
        self._last_activity = time.time()

    def mark_activity(self) -> None:
        self._last_activity = time.time()

    def is_silent(self) -> bool:
        return (time.time() - self._last_activity) >= self._threshold
