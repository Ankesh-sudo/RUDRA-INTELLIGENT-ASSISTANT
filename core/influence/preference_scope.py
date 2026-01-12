from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class PreferenceScope:
    """
    Declarative, immutable scope metadata.
    No inference. No defaults. No behavior.
    """
    applies_to: FrozenSet[str]
    contexts: FrozenSet[str]
    lifetime: str
    exclusions: FrozenSet[str]

    def validate(self) -> None:
        if not isinstance(self.lifetime, str) or not self.lifetime:
            raise ValueError("scope.lifetime must be a non-empty string")

        for name, value in [
            ("applies_to", self.applies_to),
            ("contexts", self.contexts),
            ("exclusions", self.exclusions),
        ]:
            if not isinstance(value, frozenset):
                raise ValueError(f"scope.{name} must be a frozenset")
