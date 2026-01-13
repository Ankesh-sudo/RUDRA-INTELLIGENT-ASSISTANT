from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText


class CoquiTTSEngine(TTSEngine):
    """
    Coqui TTS engine placeholder (Day 41).

    Rules:
    - No model loading
    - No audio output
    - No device access
    - No persona awareness
    - No runtime side effects

    Activation is LOCKED until Day 48.
    """

    def speak(self, text: FinalizedText) -> None:
        # Day 41: intentionally a no-op
        # This preserves architectural isolation and allows
        # future activation without refactoring.
        return
