import re

def tokenize(text: str) -> list[str]:
    """
    Lowercase, remove punctuation, split into tokens.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return [t for t in text.split() if t]
