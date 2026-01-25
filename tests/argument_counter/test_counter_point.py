import pytest
from core.argument_counter.counter_point import CounterPoint
from core.argument_counter.counter_strategy import CounterStrategy


def test_valid_counter_point():
    cp = CounterPoint(
        strategy=CounterStrategy.PREMISE_INSUFFICIENT,
        description="This relies on limited premises.",
    )
    cp.validate()


def test_emotional_language_rejected():
    with pytest.raises(ValueError):
        CounterPoint(
            strategy=CounterStrategy.ASSUMPTION_UNSTATED,
            description="I feel this is wrong.",
        ).validate()
