from typing import List
from core.argument.argument_chain import ArgumentChain
from .counter_point import CounterPoint


class CounterChain:
    """
    Holds original argument and its counter-points.
    """

    def __init__(self, argument: ArgumentChain, counters: List[CounterPoint]):
        self.argument = argument
        self.counters = counters

    def is_empty(self) -> bool:
        return len(self.counters) == 0
