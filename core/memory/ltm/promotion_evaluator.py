from dataclasses import dataclass
from enum import Enum

from core.memory.ltm.promotion_rules import (
    MemoryPromotionRules,
    PromotionDecision
)
from core.memory.ltm.consent_gate import UserConsentGate


class PromotionAction(Enum):
    PROMOTE = "promote"
    ASK_CONSENT = "ask_consent"
    IGNORE = "ignore"


@dataclass
class PromotionPlan:
    action: PromotionAction
    reason: str
    consent_prompt: str | None = None


class MemoryPromotionEvaluator:

    def __init__(self):
        self.rules = MemoryPromotionRules()
        self.consent_gate = UserConsentGate()

    def evaluate(
        self,
        confidence: float,
        repetition_count: int,
        user_confirmed: bool,
        memory_summary: str
    ) -> PromotionPlan:

        decision = self.rules.evaluate(
            confidence=confidence,
            repetition_count=repetition_count,
            user_confirmed=user_confirmed
        )

        # ---- Explicit confirmation → promote immediately ----
        if decision == PromotionDecision.PROMOTE:
            return PromotionPlan(
                action=PromotionAction.PROMOTE,
                reason="User explicitly confirmed memory",
                consent_prompt=None
            )

        # ---- Eligible for consent request ----
        if confidence > 0.85 and repetition_count >= 2:
            prompt = self.consent_gate.build_prompt(memory_summary)
            return PromotionPlan(
                action=PromotionAction.ASK_CONSENT,
                reason="High confidence and repeated signal",
                consent_prompt=prompt
            )

        # ---- Not eligible ----
        return PromotionPlan(
            action=PromotionAction.IGNORE,
            reason="Insufficient confidence or repetition",
            consent_prompt=None
        )
