from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time


class Speaker(Enum):
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class DialogueTurn:
    speaker: Speaker
    intent: Optional[str]
    context_snapshot: dict
    response_plan: str
    timestamp: float = time.time()
