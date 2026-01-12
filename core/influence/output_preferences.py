from dataclasses import dataclass
from typing import Optional, Dict
from core.influence.resolved_preferences import ResolvedPreferenceSet

# Explicit allow-list for output-only influence
ALLOWED_OUTPUT_PREFERENCES = {
    "verbosity",
    "format",
    "tone",
}

@dataclass(frozen=True)
class OutputPreferences:
    verbosity: Optional[str] = None
    format: Optional[str] = None
    tone: Optional[str] = None

    def is_empty(self) -> bool:
        return not any([self.verbosity, self.format, self.tone])


def build_output_preferences(
    resolved: ResolvedPreferenceSet,
) -> OutputPreferences:
    """
    Build a safe, read-only view of preferences for output only.
    Missing preferences => None (no defaults).
    Non-whitelisted preferences are ignored.
    """
    if resolved is None or resolved.is_empty():
        return OutputPreferences()

    values: Dict[str, Optional[str]] = {
        "verbosity": None,
        "format": None,
        "tone": None,
    }

    for key in ALLOWED_OUTPUT_PREFERENCES:
        record = resolved.get(key)
        if record is not None:
            values[key] = record.value

    return OutputPreferences(**values)
