from core.nlp.intent import Intent
from core.skills.notes import save_note, read_notes

def handle(intent: Intent, text: str = "") -> str:
    if intent == Intent.GREETING:
        return "Hello. I am Rudra."

    if intent == Intent.HELP:
        return "You can say: hi, help, save note, read notes, exit."

    if intent == Intent.NOTE_CREATE:
        return save_note(text)

    if intent == Intent.NOTE_READ:
        return read_notes()

    if intent == Intent.EXIT:
        return "Goodbye."

    return "I did not understand that."
