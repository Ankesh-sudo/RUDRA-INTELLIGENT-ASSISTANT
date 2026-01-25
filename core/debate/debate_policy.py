class DebatePolicy:
    """
    Central debate stopping rules.
    """

    MAX_TURNS = 3

    @classmethod
    def should_stop(cls, turn_index: int) -> bool:
        return turn_index >= cls.MAX_TURNS
