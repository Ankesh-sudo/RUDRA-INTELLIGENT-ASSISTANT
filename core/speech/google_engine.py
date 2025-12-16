import speech_recognition as sr
from loguru import logger


class GoogleSpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Tune for better results
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8

        logger.info("Google Speech Engine initialized")

    def listen_once(self) -> str:
        with self.microphone as source:
            logger.info("Listening (Google)...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=5,          # max wait to start speaking
                    phrase_time_limit=6 # max speech length
                )
            except sr.WaitTimeoutError:
                logger.warning("Google listen timeout")
                return ""

        try:
            text = self.recognizer.recognize_google(audio)
            logger.info("Google heard: {}", text)
            return text.lower()

        except sr.UnknownValueError:
            logger.warning("Google could not understand audio")
            return ""

        except sr.RequestError as e:
            logger.error("Google Speech API error: {}", e)
            return ""

