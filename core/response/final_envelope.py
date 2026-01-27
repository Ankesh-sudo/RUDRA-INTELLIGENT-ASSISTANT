from dataclasses import dataclass
from typing import Optional, Dict, Any
import hashlib

from core.explain.explain_surface import ExplainSurface


@dataclass(frozen=True)
class FinalResponseEnvelope:
    """
    Step 5 — Sealed response contract.

    Rules:
    - Immutable once created
    - final_text is the ONLY authoritative output
    - explain is optional, structured, and silent by default
    - persona fields are metadata ONLY (no authority)
    - Safe to log, replay, serialize
    """

    # -------------------------------------------------
    # Canonical content (single source of truth)
    # -------------------------------------------------
    final_text: str

    # -------------------------------------------------
    # Explain Surface (structured, optional)
    # -------------------------------------------------
    explain: Optional[ExplainSurface] = None

    # -------------------------------------------------
    # Persona metadata (NO authority)
    # -------------------------------------------------
    persona_applied: bool = False
    persona_hint: Optional[str] = None
    persona_fingerprint: Optional[str] = None

    # -------------------------------------------------
    # Output routing metadata
    # -------------------------------------------------
    tts_allowed: bool = True

    # -------------------------------------------------
    # Arbitrary metadata (safe, non-executable)
    # -------------------------------------------------
    meta: Optional[Dict[str, Any]] = None

    # -------------------------------------------------
    # Deterministic hash
    # -------------------------------------------------
    def text_hash(self) -> str:
        """
        Hash of canonical text only.
        Formatting, persona, explain surface MUST NOT affect this.
        """
        return hashlib.sha256(
            self.final_text.encode("utf-8")
        ).hexdigest()

    # -------------------------------------------------
    # Render helpers
    # -------------------------------------------------
    def as_text(self) -> str:
        """
        Canonical text rendering (CLI-safe).
        """
        return self.final_text

    def explain_text(self) -> Optional[str]:
        """
        Render explain surface as plain text (if enabled later).
        """
        return self.explain.as_text() if self.explain else None

    def to_dict(self) -> Dict[str, Any]:
        """
        Safe serialization for UI / API / logging.
        """
        return {
            "text": self.final_text,
            "explain": self.explain.lines if self.explain else None,
            "persona": {
                "applied": self.persona_applied,
                "hint": self.persona_hint,
                "fingerprint": self.persona_fingerprint,
            },
            "tts_allowed": self.tts_allowed,
            "meta": self.meta or {},
            "hash": self.text_hash(),
        }
