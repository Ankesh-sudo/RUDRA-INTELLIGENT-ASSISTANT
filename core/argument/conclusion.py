from dataclasses import dataclass


@dataclass(frozen=True)
class Conclusion:
    """
    Logical outcome derived from premises.
    """
    text: str
