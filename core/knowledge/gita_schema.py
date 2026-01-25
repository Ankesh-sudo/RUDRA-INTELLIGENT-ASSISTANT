from dataclasses import dataclass


@dataclass(frozen=True)
class GitaRow:
    topic: str            # e.g., "karma", "dharma"
    question: str         # canonical question
    answer: str           # exact verse meaning (no paraphrase)
    chapter: int          # 1–18
    verse: int            # verse number
    citation: str         # "Bhagavad Gita <chapter>.<verse>"
