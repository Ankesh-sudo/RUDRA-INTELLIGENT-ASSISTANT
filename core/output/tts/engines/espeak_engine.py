import subprocess
import shlex

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText


class EspeakEngine(TTSEngine):
    """
    Deterministic subprocess-based eSpeak TTS engine.
    Guaranteed to work if `espeak` works in terminal.
    Fully fail-closed and non-authoritative.
    """

    def __init__(self, voice: str = "hi"):
        self.voice = voice

    def speak(self, text: FinalizedText) -> None:
        utterance = str(text)

        cmd = f'espeak -v {self.voice} "{utterance}"'

        try:
            subprocess.run(
                shlex.split(cmd),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except Exception:
            # Absolute fail-closed: never affect assistant logic
            pass
