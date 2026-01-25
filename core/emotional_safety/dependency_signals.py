class DependencySignals:
    """
    Static dependency and manipulation signals.
    Frozen, rule-based, no ML.
    """

    # Zero tolerance (single hit = block)
    ZERO_TOLERANCE = {
        "only me",
        "you need me",
        "can't live without",
        "i will decide for you",
        "i control your",
    }

    # Accumulative signals
    EXCLUSIVE_LANGUAGE = {
        "just me",
        "me alone",
        "only i",
    }

    AUTHORITY_TRANSFER = {
        "i'll decide",
        "let me decide",
        "trust me completely",
    }

    EMOTIONAL_RELIANCE = {
        "i am all you have",
        "i am your only support",
        "you depend on me",
    }

    SELF_WORTH_SUBSTITUTION = {
        "you are nothing without",
        "i give your life meaning",
    }

    @classmethod
    def all_signals(cls) -> set[str]:
        return (
            cls.ZERO_TOLERANCE
            | cls.EXCLUSIVE_LANGUAGE
            | cls.AUTHORITY_TRANSFER
            | cls.EMOTIONAL_RELIANCE
            | cls.SELF_WORTH_SUBSTITUTION
        )
