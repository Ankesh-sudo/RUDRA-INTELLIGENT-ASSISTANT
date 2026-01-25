from core.dialogue.context_policy import ContextPolicy
from core.dialogue.session_dialogue_state import SessionDialogueState


def test_context_policy_short_ttl_for_small_talk():
    state = SessionDialogueState()
    policy = ContextPolicy()
    policy.apply(state, intent="SMALL_TALK")
    assert state.ttl_sec == policy.SHORT_TTL
