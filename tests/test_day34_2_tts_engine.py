# tests/test_day34_2_tts_engine.py

import pytest

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_engine_noop import NoOpTTSEngine
from core.output.tts.tts_contract import FinalizedText


def test_abstract_engine_cannot_be_instantiated():
    with pytest.raises(TypeError):
        TTSEngine()


def test_noop_engine_speak_returns_none():
    engine = NoOpTTSEngine()
    text = FinalizedText("hello")
    result = engine.speak(text)
    assert result is None


def test_noop_engine_does_not_mutate_text():
    engine = NoOpTTSEngine()
    text = FinalizedText("immutable")
    engine.speak(text)
    assert text.text == "immutable"
