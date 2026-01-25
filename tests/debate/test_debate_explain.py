from core.argument.argument_builder import ArgumentBuilder
from core.argument_counter.counter_builder import CounterBuilder
from core.debate.debate_orchestrator import DebateOrchestrator
from core.debate.debate_explain import DebateExplain


def test_debate_explain_output():
    argument = ArgumentBuilder().build(
        "Water boils at 100°C",
        ["At sea level, water boils at 100°C"],
    )
    counters = CounterBuilder().build(argument)

    turns, state = DebateOrchestrator().run(argument, counters)
    text = DebateExplain.format(turns, state)

    assert "Debate ended:" in text
