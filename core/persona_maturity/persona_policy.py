class PersonaPolicy:
    """
    Declarative persona limits (THE LAW).
    """

    # Hard caps
    MAX_SENTENCE_LENGTH = 200
    MAX_AFFECTION_MARKERS = 1  # e.g., ❤️, <3

    # Forbidden dependency / manipulation phrases
    FORBIDDEN_PHRASES = {
        "you need me",
        "only me",
        "can't live without",
        "depend on me",
        "i control",
    }

    # Allowed affection markers (counted)
    AFFECTION_MARKERS = {"❤️", "<3"}

    # Allowed modes (static)
    ALLOWED_MODES = {"neutral", "best_friend", "warrior"}
