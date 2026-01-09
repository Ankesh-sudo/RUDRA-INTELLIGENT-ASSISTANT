"""
Confidence Adjuster

Applies small, capped confidence boosts using memory signals.
Rule-based and deterministic.
"""

class ConfidenceAdjuster:
    MAX_BOOST = 0.10   # absolute cap
    MAX_CONFIDENCE = 0.90

    def adjust(
        self,
        *,
        base_confidence: float,
        intent: str,
        context_pack: dict
    ) -> float:
        """
        Return adjusted confidence (never lower, never exceed caps).
        """

        confidence = base_confidence
        boost = 0.0

        # Signal 1: recent conversation continuity
        recent = context_pack.get("recent_conversation", [])
        if recent:
            last = recent[-1]
            if last.get("intent") == intent:
                boost += 0.05

        # Signal 2: user preference relevance
        prefs = context_pack.get("user_preferences", [])
        for pref in prefs:
            if pref.get("intent") == intent:
                boost += 0.03
                break

        # Apply caps
        boost = min(boost, self.MAX_BOOST)
        confidence = min(confidence + boost, self.MAX_CONFIDENCE)

        return confidence
