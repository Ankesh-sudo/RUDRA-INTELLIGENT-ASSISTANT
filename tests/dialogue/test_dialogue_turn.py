from core.dialogue.dialogue_turn import DialogueTurn, Speaker
from core.dialogue.dialogue_types import DialogueIntent


def test_dialogue_turn_is_immutable():
    turn = DialogueTurn(
        speaker=Speaker.ASSISTANT,
        intent=DialogueIntent.SMALL_TALK,
        context_snapshot={},
        response_plan="ok",
    )

    assert turn.response_plan == "ok"
    assert turn.intent == DialogueIntent.SMALL_TALK
    assert turn.speaker == Speaker.ASSISTANT
