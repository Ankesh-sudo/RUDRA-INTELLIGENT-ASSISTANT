import speech_recognition as sr
from loguru import logger


class GoogleSpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=9)
        logger.info("Google Speech Engine initialized")

    def listen_once(self) -> str:
        with self.microphone as source:
            logger.info("Listening (Google)...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            logger.info("Google heard: {}", text)
            return text
        except Exception:
            return ""
