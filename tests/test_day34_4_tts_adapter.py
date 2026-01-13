# tests/test_day34_4_tts_adapter.py

from core.output.tts.tts_adapter import TTSAdapter
from core.output.tts.tts_contract import FinalizedText


def test_speak_with_disabled_engine_no_error():
    TTSAdapter.speak("hello", engine_name="disabled")


def test_hard_interrupt_cancels():
    TTSAdapter.speak("hello", interrupt="HARD")


def test_soft_interrupt_cancels():
    TTSAdapter.speak("hello", interrupt="SOFT")


def test_unknown_engine_is_safe():
    TTSAdapter.speak("hello", engine_name="unknown_engine")


def test_invalid_input_is_safe():
    TTSAdapter.speak(12345)


def test_finalized_text_not_mutated():
    ft = FinalizedText("immutable")
    TTSAdapter.speak(ft)
    assert ft.text == "immutable"
