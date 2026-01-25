from enum import Enum


class CounterStrategy(str, Enum):
    """
    Allowed counter-argument strategies.
    """

    PREMISE_INSUFFICIENT = "premise_insufficient"
    ASSUMPTION_UNSTATED = "assumption_unstated"
    SCOPE_LIMITATION = "scope_limitation"
