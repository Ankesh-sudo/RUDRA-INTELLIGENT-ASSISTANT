from sqlalchemy import select
from core.storage.mysql import get_session
from core.storage.notes_models import Note

def save_note(text: str) -> str:
    # Remove command keywords
    lowered = text.lower()
    for phrase in ["save note", "write note", "take note"]:
        if lowered.startswith(phrase):
            content = text[len(phrase):].strip()
            break
    else:
        content = text.strip()

    if not content:
        return "What should I save in the note?"

    with get_session() as session:
        session.add(Note(content=content))

    return "Note saved."


def read_notes(limit: int = 5) -> str:
    with get_session() as session:
        stmt = select(Note.content).order_by(Note.created_at.desc()).limit(limit)
        notes = session.execute(stmt).scalars().all()

    if not notes:
        return "You have no notes."

    response = "Your recent notes:\n"
    for i, content in enumerate(notes, 1):
        response += f"{i}. {content}\n"

    return response.strip()
