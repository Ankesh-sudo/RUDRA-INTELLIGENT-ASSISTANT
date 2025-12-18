WAKE_WORD = "rudra"

def contains_wake_word(text: str) -> bool:
    if not text:
        return False
    return WAKE_WORD in text.lower()
