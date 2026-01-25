from core.dialogue.fast_path import FastPath


def test_fast_path_skips_for_short_text_with_cache():
    fp = FastPath()
    assert fp.can_skip_intent_resolution("SMALL_TALK", "ok") is True
    assert fp.can_skip_intent_resolution(None, "ok") is False
