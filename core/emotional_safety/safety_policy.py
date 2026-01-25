class SafetyPolicy:
    """
    Declarative emotional safety rules (THE LAW).
    """

    # Any zero tolerance signal = immediate block
    ZERO_TOLERANCE_ENABLED = True

    # Max allowed non-zero signals before block
    MAX_SIGNAL_HITS = 1
