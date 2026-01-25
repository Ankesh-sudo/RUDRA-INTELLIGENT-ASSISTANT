from dataclasses import dataclass


@dataclass(frozen=True)
class UpanishadRow:
    topic: str
    question: str
    answer: str
    text: str        # e.g., "Isha Upanishad"
    verse: str       # e.g., "1"
    citation: str    # e.g., "Isha Upanishad 1"
