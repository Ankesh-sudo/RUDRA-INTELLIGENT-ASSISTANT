from core.memory.ltm.promotion_evaluator import (
    MemoryPromotionEvaluator,
    PromotionAction
)


def test_promote_on_user_confirmation():
    evaluator = MemoryPromotionEvaluator()
    plan = evaluator.evaluate(
        confidence=0.2,
        repetition_count=0,
        user_confirmed=True,
        memory_summary="user likes Chrome"
    )
    assert plan.action == PromotionAction.PROMOTE


def test_ask_consent_on_high_confidence_and_repetition():
    evaluator = MemoryPromotionEvaluator()
    plan = evaluator.evaluate(
        confidence=0.9,
        repetition_count=2,
        user_confirmed=False,
        memory_summary="user prefers Chrome"
    )
    assert plan.action == PromotionAction.ASK_CONSENT


def test_ignore_on_low_signal():
    evaluator = MemoryPromotionEvaluator()
    plan = evaluator.evaluate(
        confidence=0.4,
        repetition_count=1,
        user_confirmed=False,
        memory_summary="user opened Chrome once"
    )
    assert plan.action == PromotionAction.IGNORE
