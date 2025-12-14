from core.nlp.intent import Intent

def handle(intent: Intent) -> str:
    if intent == Intent.GREETING:
        return "Hello. I am Rudra."

    if intent == Intent.HELP:
        return "You can say: hi, help, exit."

    if intent == Intent.EXIT:
        return "Goodbye."

    return "I did not understand that."
