from dataclasses import dataclass
from typing import Optional
import hashlib


@dataclass(frozen=True)
class FinalResponseEnvelope:
    """
    Sealed, immutable carrier between logic and presentation layers.

    - final_text is canonical and authoritative
    - persona_hint is optional metadata for phrasing only
    - persona_applied indicates whether persona rendering was used
    - persona_fingerprint is for traceability only (no authority)
    - tts_allowed is a downstream signal, not a command
    """

    # Canonical output (single source of truth)
    final_text: str

    # Persona-related metadata (NO authority)
    persona_applied: bool
    persona_hint: Optional[str] = None
    persona_fingerprint: Optional[str] = None

    # Output routing flag
    tts_allowed: bool = True

    def text_hash(self) -> str:
        """
        Hash of canonical text only.
        Persona phrasing MUST NOT affect this.
        """
        return hashlib.sha256(
            self.final_text.encode("utf-8")
        ).hexdigest()
