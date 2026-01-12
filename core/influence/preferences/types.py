from dataclasses import dataclass
from typing import Any
from core.influence.preference_scope import PreferenceScope

@dataclass(frozen=True)
class Preference:
    """
    Immutable user preference.
    Declarative only — no behavior.
    """
    key: str
    value: Any
    scope: PreferenceScope
