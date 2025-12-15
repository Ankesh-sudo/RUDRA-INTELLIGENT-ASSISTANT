from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, Text, DateTime, func
from core.storage.mysql import get_engine

BaseNotes = declarative_base()

class Note(BaseNotes):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

# Create table
engine = get_engine()
BaseNotes.metadata.create_all(bind=engine)
