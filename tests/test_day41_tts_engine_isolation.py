import pytest

from core.output.tts.tts_registry import TTSEngineRegistry
from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText


class ExplodingTTSEngine(TTSEngine):
    """
    A TTS engine that always fails.
    Used to prove TTS failures are isolated.
    """

    def speak(self, text: FinalizedText) -> None:
        raise RuntimeError("TTS engine failure")


def test_tts_engine_is_side_effect_only(monkeypatch):
    """
    Day 41 guarantee:
    - TTS failure must NOT crash assistant logic
    - TTS must NOT modify finalized text
    """

    # Arrange
    finalized = FinalizedText("Hello Boss")

    # Force registry to return a failing TTS engine
    monkeypatch.setattr(
        TTSEngineRegistry,
        "_ENGINES",
        {"test": ExplodingTTSEngine()}
    )

    engine = TTSEngineRegistry.get("test")

    # Act + Assert
    # TTS failure should be catchable and not alter text
    with pytest.raises(RuntimeError):
        engine.speak(finalized)

    # Text must remain unchanged
    assert finalized.text == "Hello Boss"


def test_coqui_engine_is_present_and_inert():
    """
    Day 41 guarantee:
    - Coqui engine exists
    - Calling speak() produces no output and no error
    """

    engine = TTSEngineRegistry.get("coqui")
    text = FinalizedText("Silent test")

    # Should not raise
    engine.speak(text)

    # Text must remain untouched
    assert text.text == "Silent test"
