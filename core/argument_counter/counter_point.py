from dataclasses import dataclass
from .counter_strategy import CounterStrategy


@dataclass(frozen=True)
class CounterPoint:
    """
    One logical counter point.
    """
    strategy: CounterStrategy
    description: str

    def validate(self) -> None:
        if not self.description or not self.description.strip():
            raise ValueError("Counter description cannot be empty")

        banned = ["feel", "believe", "emotion", "obviously", "clearly"]
        for word in banned:
            if word in self.description.lower():
                raise ValueError("Emotional or persuasive language detected")
