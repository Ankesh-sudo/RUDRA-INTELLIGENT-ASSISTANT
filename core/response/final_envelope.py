from dataclasses import dataclass
from typing import Optional
import hashlib


@dataclass(frozen=True)
class FinalResponseEnvelope:
    """
    Sealed, immutable carrier between text and voice.
    Single source of truth for final output.
    """
    final_text: str
    persona_applied: bool
    persona_fingerprint: Optional[str]
    tts_allowed: bool

    def text_hash(self) -> str:
        return hashlib.sha256(self.final_text.encode("utf-8")).hexdigest()
