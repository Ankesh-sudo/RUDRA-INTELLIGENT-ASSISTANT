# core/metrics/latency_timer.py

import time
from contextlib import contextmanager


class LatencyTimer:
    """
    Day 75 — Monotonic latency timer.

    Observability only.
    No behavior change.
    """

    @contextmanager
    def measure(self):
        start = time.monotonic()
        yield lambda: time.monotonic() - start
