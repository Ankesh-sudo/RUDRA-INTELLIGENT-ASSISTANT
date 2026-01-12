from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class PreferenceResolutionRecord:
    key: str
    value: Any
    source: str
    reason: str
    rejected: List[Dict[str, Any]]


@dataclass(frozen=True)
class ResolvedPreferenceSet:
    preferences: Dict[str, PreferenceResolutionRecord]

    def get(self, key: str):
        return self.preferences.get(key)

    def keys(self):
        return list(self.preferences.keys())

    def is_empty(self) -> bool:
        return not bool(self.preferences)
