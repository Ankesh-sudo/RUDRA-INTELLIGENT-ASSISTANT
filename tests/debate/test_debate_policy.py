from core.debate.debate_policy import DebatePolicy


def test_policy_max_turns():
    assert DebatePolicy.should_stop(3) is True
    assert DebatePolicy.should_stop(1) is False
