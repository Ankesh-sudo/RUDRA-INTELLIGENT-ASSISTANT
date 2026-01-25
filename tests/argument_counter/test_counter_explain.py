from core.argument.argument_builder import ArgumentBuilder
from core.argument_counter.counter_builder import CounterBuilder
from core.argument_counter.counter_explain import CounterExplain


def test_counter_explanation_format():
    arg = ArgumentBuilder().build(
        "Water boils at 100°C",
        ["At sea level, water boils at 100°C"],
    )

    counter_chain = CounterBuilder().build(arg)
    text = CounterExplain.format(counter_chain)

    assert "Original Claim:" in text
    assert "Counter Points:" in text or "No strong counter-argument" in text
