import pyttsx3

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText


class Pyttsx3Engine(TTSEngine):
    def __init__(self, voice_hint: str = "hi"):
        self.engine = pyttsx3.init(driverName="espeak")

        selected = False
        for voice in self.engine.getProperty("voices"):
            if voice_hint in voice.id.lower():
                self.engine.setProperty("voice", voice.id)
                selected = True
                break

        if not selected:
            print("[WARN] Voice not found, using default")

        self.engine.setProperty("rate", 155)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text: FinalizedText) -> None:
        self.engine.say(str(text))
        self.engine.runAndWait()
