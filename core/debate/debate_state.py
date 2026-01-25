class DebateState:
    """
    Tracks debate execution state.
    """

    def __init__(self, max_turns: int):
        self.max_turns = max_turns
        self.current_turn = 0
        self.terminated = False
        self.termination_reason: str | None = None

    def stop(self, reason: str) -> None:
        self.terminated = True
        self.termination_reason = reason
