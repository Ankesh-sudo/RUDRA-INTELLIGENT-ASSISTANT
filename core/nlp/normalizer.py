import re

# Expanded filler words (safe to grow)
FILLER_WORDS = {
    "um", "uh", "hmm",
    "please", "hey",
    "okay", "ok", "ya", "yeah",
    "can", "you", "could", "would", "kindly"
}

# Reference normalization (NO execution here)
REFERENCE_MAP = {
    "again": "__REPEAT__",
    "it": "__REF__"
}


def normalize_text(text: str) -> list[str]:
    """
    Day 14.2 Normalizer
    - lowercase
    - remove punctuation
    - remove filler words
    - normalize simple references
    - return clean token list
    """

    if not text:
        return []

    # lowercase
    text = text.lower()

    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    words = text.split()
    normalized = []

    for w in words:
        if w in FILLER_WORDS:
            continue
        if w in REFERENCE_MAP:
            normalized.append(REFERENCE_MAP[w])
        else:
            normalized.append(w)

    return normalized
