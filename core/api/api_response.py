from dataclasses import dataclass
from datetime import datetime
from typing import Any
from .api_errors import APIInvalidResponse


@dataclass(frozen=True)
class APIResponse:
    data: Any
    source: str
    timestamp: str

    @classmethod
    def build(cls, data: Any, source: str):
        if data is None:
            raise APIInvalidResponse("Response data is missing")

        return cls(
            data=data,
            source=source,
            timestamp=datetime.utcnow().isoformat(),
        )
