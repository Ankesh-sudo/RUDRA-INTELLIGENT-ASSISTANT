from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PreferenceType(Enum):
    TONE = "tone"
    VERBOSITY = "verbosity"
    LANGUAGE = "language"
    FORMAT = "format"
    THEME = "theme"


class InfluenceStrength(Enum):
    SOFT = "soft"       # advisory only
    NONE = "none"       # default / no influence


@dataclass(frozen=True)
class PreferenceInfluence:
    """
    Describes a single, safe, non-behavioral preference influence.
    """
    pref_type: PreferenceType
    value: str
    strength: InfluenceStrength = InfluenceStrength.SOFT
    source: str = "memory"
    confidence: float = 1.0

    def is_active(self) -> bool:
        return self.strength == InfluenceStrength.SOFT

    def explain(self) -> str:
        return (
            f"Preference influence detected: {self.pref_type.value} = '{self.value}' "
            f"(strength={self.strength.value}, source={self.source})"
        )
