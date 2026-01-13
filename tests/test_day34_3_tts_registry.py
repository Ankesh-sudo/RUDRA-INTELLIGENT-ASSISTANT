# tests/test_day34_3_tts_registry.py

import pytest

from core.output.tts.tts_registry import TTSEngineRegistry, TTSEngineNotFound
from core.output.tts.tts_engine import TTSEngine


def test_disabled_engine_resolves():
    engine = TTSEngineRegistry.get("disabled")
    assert isinstance(engine, TTSEngine)


def test_noop_engine_resolves():
    engine = TTSEngineRegistry.get("noop")
    assert isinstance(engine, TTSEngine)


def test_unknown_engine_raises():
    with pytest.raises(TTSEngineNotFound):
        TTSEngineRegistry.get("espeak")


def test_non_string_engine_name_raises():
    with pytest.raises(TTSEngineNotFound):
        TTSEngineRegistry.get(123)
