from loguru import logger
from core.storage.mysql import verify_connection
from core.input.text_input import read_text
from core.nlp.tokenizer import tokenize
from core.nlp.intent import detect_intent, Intent
from core.skills.basic import handle

class Assistant:
    def __init__(self):
        self.name = "Rudra"
        self.running = True

    def run(self):
        logger.info("Assistant initialized: {}", self.name)

        ok, msg = verify_connection()
        if ok:
            logger.info("MySQL connection OK: {}", msg)
        else:
            logger.error("MySQL connection FAILED: {}", msg)

        logger.info("Day 2 started. Text command engine ready.")

        while self.running:
            text = read_text()
            tokens = tokenize(text)
            intent = detect_intent(tokens)
            response = handle(intent)

            print(f"Rudra > {response}")

            if intent == Intent.EXIT:
                self.running = False

        logger.info("Day 2 complete.")
