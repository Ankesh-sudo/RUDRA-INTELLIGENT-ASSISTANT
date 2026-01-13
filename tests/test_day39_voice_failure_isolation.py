import pytest

from core.output.tts.tts_adapter import TTSAdapter


class ExplodingEngine:
    def speak(self, text):
        raise RuntimeError("tts boom")


def test_day39_tts_failure_is_fully_isolated(monkeypatch):
    """
    Day 39 proof test.

    Guarantees:
    - TTS crash is fully contained
    - No exception escapes
    - Call returns cleanly (fail-closed)
    """

    # Force registry to return exploding engine
    monkeypatch.setattr(
        "core.output.tts.tts_registry.TTSEngineRegistry.get",
        lambda _: ExplodingEngine()
    )

    # MUST NOT crash, MUST swallow exception
    TTSAdapter.speak(
        "immutable response",
        engine_name="explode",
        interrupt=None,
    )

    # If we reach here, Day 39 invariant holds
    assert True
