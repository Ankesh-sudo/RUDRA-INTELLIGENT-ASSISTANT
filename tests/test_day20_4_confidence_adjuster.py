from core.memory.confidence_adjuster import ConfidenceAdjuster


def test_confidence_never_decreases():
    adj = ConfidenceAdjuster()
    base = 0.7
    out = adj.adjust(
        base_confidence=base,
        intent="greeting",
        context_pack={}
    )
    assert out >= base


def test_confidence_caps_applied():
    adj = ConfidenceAdjuster()
    context = {
        "recent_conversation": [{"intent": "greeting"}],
        "user_preferences": [{"intent": "greeting"}]
    }
    out = adj.adjust(
        base_confidence=0.88,
        intent="greeting",
        context_pack=context
    )
    assert out <= adj.MAX_CONFIDENCE
