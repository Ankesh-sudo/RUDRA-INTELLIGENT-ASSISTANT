from core.memory.ltm.promotion_evaluator import (
    MemoryPromotionEvaluator,
    PromotionAction
)


def test_consent_prompt_generated_for_ask_consent():
    evaluator = MemoryPromotionEvaluator()
    plan = evaluator.evaluate(
        confidence=0.9,
        repetition_count=2,
        user_confirmed=False,
        memory_summary="you prefer Chrome"
    )

    assert plan.action == PromotionAction.ASK_CONSENT
    assert plan.consent_prompt is not None
    assert "remember" in plan.consent_prompt.lower()


def test_no_consent_prompt_for_promote():
    evaluator = MemoryPromotionEvaluator()
    plan = evaluator.evaluate(
        confidence=0.3,
        repetition_count=0,
        user_confirmed=True,
        memory_summary="your name is Ankesh"
    )

    assert plan.action == PromotionAction.PROMOTE
    assert plan.consent_prompt is None


def test_no_consent_prompt_for_ignore():
    evaluator = MemoryPromotionEvaluator()
    plan = evaluator.evaluate(
        confidence=0.4,
        repetition_count=1,
        user_confirmed=False,
        memory_summary="opened Chrome once"
    )

    assert plan.action == PromotionAction.IGNORE
    assert plan.consent_prompt is None
