import time
from core.dialogue.session_dialogue_state import SessionDialogueState


def test_session_state_updates_and_expires():
    state = SessionDialogueState(ttl_sec=0.05)
    state.update(topic="greeting", intent="SMALL_TALK")

    assert state.topic == "greeting"
    assert state.last_intent == "SMALL_TALK"

    time.sleep(0.06)
    assert state.is_expired()

    state.reset_if_expired()
    assert state.topic is None
    assert state.last_intent is None
