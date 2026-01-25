from dataclasses import dataclass
from enum import Enum


class DebateSpeaker(str, Enum):
    ARGUMENT = "argument"
    COUNTER = "counter"


@dataclass(frozen=True)
class DebateTurn:
    """
    Immutable debate turn.
    """
    index: int
    speaker: DebateSpeaker
    content: str
