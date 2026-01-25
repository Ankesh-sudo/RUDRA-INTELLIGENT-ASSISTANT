from .debate_state import DebateState
from .debate_turn import DebateTurn


class DebateExplain:
    """
    Formats debate trace.
    """

    @staticmethod
    def format(turns: list[DebateTurn], state: DebateState) -> str:
        lines = []
        for turn in turns:
            lines.append(f"{turn.index}. [{turn.speaker}] {turn.content}")

        if state.termination_reason:
            lines.append(f"Debate ended: {state.termination_reason}")

        return "\n".join(lines)
