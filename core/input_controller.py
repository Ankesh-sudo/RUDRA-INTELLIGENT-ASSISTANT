from core.config import INPUT_MODE, PUSH_TO_TALK
from core.input.text_input import read_text
from core.speech.google_engine import GoogleSpeechEngine


class InputController:
    def __init__(self):
        self.voice = GoogleSpeechEngine()

    def read(self) -> str:
        if INPUT_MODE == "text":
            return read_text()

        if INPUT_MODE == "voice":
            if PUSH_TO_TALK:
                input("Press ENTER to speak...")
            return self.voice.listen_once()

        return ""
