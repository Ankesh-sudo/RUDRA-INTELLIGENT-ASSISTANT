from typing import List
from .dependency_signals import DependencySignals


class SafetyDetector:
    """
    Deterministic signal detector.
    """

    @staticmethod
    def detect(text: str) -> List[str]:
        if not isinstance(text, str):
            return []

        lowered = text.lower()
        hits = []

        for signal in DependencySignals.all_signals():
            if signal in lowered:
                hits.append(signal)

        return hits
