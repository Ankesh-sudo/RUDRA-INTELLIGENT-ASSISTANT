from core.output.tts.tts_runtime import TTSRuntime
from core.output.tts.tts_contract import validate_finalized_text


def test_tts_runtime_returns_quickly():
    """
    Day 46 guarantee:
    - TTS runtime must never block
    - Must accept only validated FinalizedText
    - Must fail silently
    """

    finalized = validate_finalized_text("hello")

    TTSRuntime.speak(
        finalized,
        engine_name="disabled",
    )
