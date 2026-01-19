import re
from typing import List

CONNECTORS = [
    r"\band then\b",
    r"\bthen\b",
    r"\band\b",
    r"\bafter that\b",
    r"\bnext\b",
]

class IntentSplitter:
    def split(self, text: str) -> List[str]:
        normalized = text.lower().strip()

        pattern = "|".join(CONNECTORS)
        parts = re.split(pattern, normalized)

        return [p.strip() for p in parts if p.strip()]
