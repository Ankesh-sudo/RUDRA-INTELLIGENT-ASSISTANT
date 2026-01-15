SYSTEM_WORDS = {"exit", "quit", "help", "repeat", "again"}

STOPWORDS = {
    "the", "is", "am", "are", "was", "were",
    "to", "of", "and", "a", "an"
}

def is_input_valid(text: str) -> bool:
    """
    Day 50 – Voice-safe quality gate
    - Allows single-word slot replies (e.g. 'chrome')
    - Blocks empty / noise
    """

    if not text:
        return False

    words = text.lower().split()

    # system commands
    if len(words) == 1 and words[0] in SYSTEM_WORDS:
        return True

    # 🔑 allow single-word slot answers
    if len(words) == 1:
        return True

    if len(text) < 3:
        return False

    meaningful = [w for w in words if w not in STOPWORDS]
    return len(meaningful) > 0
