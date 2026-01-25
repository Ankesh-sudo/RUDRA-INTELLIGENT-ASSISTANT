from dataclasses import dataclass


@dataclass(frozen=True)
class DharmaRow:
    topic: str          # e.g., "dharma"
    question: str       # canonical question
    answer: str         # exact answer text
    citation: str       # e.g., "Bhagavad Gita 2.47"
