from typing import List
from core.argument.argument_chain import ArgumentChain
from core.argument_counter.counter_chain import CounterChain
from .debate_turn import DebateTurn, DebateSpeaker
from .debate_state import DebateState
from .debate_policy import DebatePolicy


class DebateOrchestrator:
    """
    Coordinates argument and counter-argument exchange.
    """

    def run(
        self,
        argument: ArgumentChain,
        counter_chain: CounterChain,
    ) -> tuple[List[DebateTurn], DebateState]:

        state = DebateState(max_turns=DebatePolicy.MAX_TURNS)
        turns: List[DebateTurn] = []

        # Turn 1 — Argument summary
        turns.append(
            DebateTurn(
                index=1,
                speaker=DebateSpeaker.ARGUMENT,
                content=argument.conclusion.text,
            )
        )
        state.current_turn = 1

        # No counters → stop immediately
        if counter_chain.is_empty():
            state.stop("No counter-arguments available")
            return turns, state

        # Counter turns
        for counter in counter_chain.counters:
            if DebatePolicy.should_stop(state.current_turn):
                state.stop("Maximum turns reached")
                break

            state.current_turn += 1
            turns.append(
                DebateTurn(
                    index=state.current_turn,
                    speaker=DebateSpeaker.COUNTER,
                    content=counter.description,
                )
            )

        if not state.terminated:
            state.stop("Counters exhausted")

        return turns, state
