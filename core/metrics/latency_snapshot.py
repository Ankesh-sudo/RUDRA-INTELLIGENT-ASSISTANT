# core/metrics/latency_snapshot.py

from dataclasses import dataclass


@dataclass(frozen=True)
class LatencySnapshot:
    """
    Day 75 — Immutable latency snapshot.

    - In-memory only
    - Not stored
    - Not spoken
    """

    dialogue_ms: float = 0.0
    speech_ms: float = 0.0
    total_ms: float = 0.0
