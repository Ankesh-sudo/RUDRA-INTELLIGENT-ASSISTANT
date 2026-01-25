from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class AdapterResponse:
    """
    Normalized adapter output.
    """
    title: str
    payload: Dict[str, Any]
    source: str
    timestamp: str

    @classmethod
    def build(cls, title: str, payload: Dict[str, Any], source: str):
        if not title or not isinstance(payload, dict) or not source:
            raise ValueError("Invalid adapter response fields")

        return cls(
            title=title,
            payload=payload,
            source=source,
            timestamp=datetime.utcnow().isoformat(),
        )
