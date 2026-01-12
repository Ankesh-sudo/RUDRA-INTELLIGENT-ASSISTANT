from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PersonaInput:
    """
    Strict contract for persona layer.
    Persona receives ONLY final text + optional presentation hints.
    """
    text: str
    language: str = "en"
    tone_hint: Optional[str] = None
