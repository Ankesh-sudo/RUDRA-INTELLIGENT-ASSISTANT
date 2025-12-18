from core.speech.google_engine import GoogleSpeechEngine


class InputController:
    def __init__(self):
        self.speech = GoogleSpeechEngine()

    def read(self) -> str:
        input("Press ENTER to speak...")
        return self.speech.listen_once()
