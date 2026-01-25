from typing import List
from core.argument.argument_chain import ArgumentChain
from .counter_point import CounterPoint
from .counter_strategy import CounterStrategy
from .counter_chain import CounterChain


class CounterBuilder:
    """
    Deterministic counter-argument generator.
    """

    MAX_COUNTERS = 2

    def build(self, argument: ArgumentChain) -> CounterChain:
        counters: List[CounterPoint] = []

        premise_count = len(argument.premises)

        # Rule 1: Single premise → possible insufficiency
        if premise_count == 1:
            counters.append(
                CounterPoint(
                    strategy=CounterStrategy.PREMISE_INSUFFICIENT,
                    description="The conclusion relies on a single premise, which may be insufficient to fully support it.",
                )
            )

        # Rule 2: Check for unstated assumptions
        if premise_count >= 1:
            counters.append(
                CounterPoint(
                    strategy=CounterStrategy.ASSUMPTION_UNSTATED,
                    description="The argument assumes conditions that are not explicitly stated in the premises.",
                )
            )

        # Cap counters
        counters = counters[: self.MAX_COUNTERS]

        # Validate counters
        for counter in counters:
            counter.validate()

        return CounterChain(argument=argument, counters=counters)
