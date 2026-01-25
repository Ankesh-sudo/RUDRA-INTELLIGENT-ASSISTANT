from core.argument_counter.counter_strategy import CounterStrategy


def test_counter_strategy_values():
    assert CounterStrategy.PREMISE_INSUFFICIENT.value == "premise_insufficient"
