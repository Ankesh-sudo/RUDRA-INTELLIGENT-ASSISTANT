from core.dialogue.minimal_questioning import MinimalQuestioning


def test_minimal_questioning_rules():
    mq = MinimalQuestioning()
    assert mq.should_ask("UNKNOWN", False) is True
    assert mq.should_ask("SMALL_TALK", False) is False
    assert mq.should_ask("SMALL_TALK", True) is True
