from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PersonaTrace:
    persona_name: str
    original_text: str
    transformed_text: str
    tone_applied: str
    timestamp: datetime
