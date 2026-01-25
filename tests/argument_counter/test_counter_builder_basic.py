from core.argument.argument_builder import ArgumentBuilder
from core.argument_counter.counter_builder import CounterBuilder


def test_counter_generated_for_single_premise():
    arg = ArgumentBuilder().build(
        "Water boils at 100°C",
        ["At sea level, water boils at 100°C"],
    )

    chain = CounterBuilder().build(arg)
    assert len(chain.counters) >= 1
