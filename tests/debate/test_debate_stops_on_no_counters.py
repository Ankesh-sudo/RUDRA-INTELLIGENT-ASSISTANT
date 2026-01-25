from core.argument.argument_builder import ArgumentBuilder
from core.argument_counter.counter_chain import CounterChain
from core.debate.debate_orchestrator import DebateOrchestrator


def test_stop_when_no_counters():
    argument = ArgumentBuilder().build(
        "The sun rises in the east",
        ["Earth rotates west to east"],
    )

    empty_counters = CounterChain(argument, [])
    turns, state = DebateOrchestrator().run(argument, empty_counters)

    assert state.termination_reason == "No counter-arguments available"
