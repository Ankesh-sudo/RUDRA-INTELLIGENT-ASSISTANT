from loguru import logger

def read_text() -> str:
    try:
        text = input("You > ").strip()
        logger.debug("Text input received: {}", text)
        return text
    except KeyboardInterrupt:
        return "exit"
