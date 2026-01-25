from core.argument.argument_builder import ArgumentBuilder
from core.argument_counter.counter_builder import CounterBuilder


def test_counter_chain_exists_even_if_limited():
    arg = ArgumentBuilder().build(
        "Gravity attracts objects",
        [
            "Objects with mass exert gravitational force",
            "This force causes attraction between masses",
        ],
    )

    chain = CounterBuilder().build(arg)
    assert chain is not None
