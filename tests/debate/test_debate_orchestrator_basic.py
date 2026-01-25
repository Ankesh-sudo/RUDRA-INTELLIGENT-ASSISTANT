from core.argument.argument_builder import ArgumentBuilder
from core.argument_counter.counter_builder import CounterBuilder
from core.debate.debate_orchestrator import DebateOrchestrator


def test_basic_debate_flow():
    argument = ArgumentBuilder().build(
        "Water boils at 100°C",
        ["At sea level, water boils at 100°C"],
    )
    counters = CounterBuilder().build(argument)

    turns, state = DebateOrchestrator().run(argument, counters)

    assert len(turns) >= 1
    assert state.terminated is True
