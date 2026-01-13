# core/persona/profile.py

from dataclasses import dataclass
import hashlib
from typing import Tuple


@dataclass(frozen=True)
class PersonaProfile:
    """
    Immutable persona identity.
    This defines WHO the persona is — not what it does.
    """

    name: str
    version: str
    affection_tier: str  # must be "A"
    suffixes: Tuple[str, ...]

    def fingerprint(self) -> str:
        """
        Stable identity hash.
        Any change to persona definition changes this fingerprint.
        """
        raw = f"{self.name}|{self.version}|{self.affection_tier}|{self.suffixes}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
