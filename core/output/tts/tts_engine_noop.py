# core/output/tts/tts_engine_noop.py

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText


class NoOpTTSEngine(TTSEngine):
    """
    Default TTS engine.
    Intentionally does nothing.
    """

    def speak(self, text: FinalizedText) -> None:
        # Explicit no-op: text is already authoritative
        return None
