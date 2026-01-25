from core.debate.debate_turn import DebateTurn, DebateSpeaker


def test_debate_turn_immutable():
    turn = DebateTurn(1, DebateSpeaker.ARGUMENT, "Test")
    assert turn.index == 1
    assert turn.speaker == DebateSpeaker.ARGUMENT
