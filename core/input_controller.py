from loguru import logger
from core.speech.google_engine import GoogleSpeechEngine
from core.speech.wake_word import contains_wake_word

class InputController:
    def __init__(self):
        self.speech = GoogleSpeechEngine()

    def read(self) -> str:
        input("Press ENTER and say 'rudra'...")

        text = self.speech.listen_once()
        logger.debug("Raw speech: {}", text)

        if not contains_wake_word(text):
            print("Rudra > (wake word not detected)")
            return ""

        # Remove wake word from command
        clean_text = text.lower().replace("rudra", "").strip()

        logger.debug("Wake-word accepted, command: {}", clean_text)
        return clean_text
