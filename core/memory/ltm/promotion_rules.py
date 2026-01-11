from enum import Enum

class PromotionDecision(Enum):
    PROMOTE = "promote"
    HOLD = "hold"
    REJECT = "reject"

class MemoryPromotionRules:

    def evaluate(
        self,
        confidence: float,
        repetition_count: int,
        user_confirmed: bool
    ) -> PromotionDecision:

        if user_confirmed:
            return PromotionDecision.PROMOTE

        return PromotionDecision.HOLD
