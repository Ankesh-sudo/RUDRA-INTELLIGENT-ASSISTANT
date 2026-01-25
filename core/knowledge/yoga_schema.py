from dataclasses import dataclass


@dataclass(frozen=True)
class YogaSutraRow:
    topic: str
    question: str
    answer: str
    chapter: int     # 1–4
    sutra: int       # ≥1
    citation: str    # e.g., "Yoga Sutra 1.2"
