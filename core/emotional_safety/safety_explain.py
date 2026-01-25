from .safety_decision import SafetyDecision


class SafetyExplain:
    """
    Explainability surface for emotional safety.
    """

    @staticmethod
    def explain(
        *,
        text: str,
        detected_signals: list[str],
        decision: SafetyDecision,
    ) -> dict:
        return {
            "input_text": text,
            "detected_signals": detected_signals,
            "outcome": decision.outcome.value,
            "reason": decision.reason,
        }
