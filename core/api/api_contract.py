from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class APIContract:
    """
    Immutable API request definition.
    """
    name: str
    endpoint: str
    method: str
    params_schema: Dict[str, type]
    read_only: bool = True

    def validate(self) -> None:
        if not self.name or not self.endpoint:
            raise ValueError("APIContract requires name and endpoint")

        if self.method.upper() not in ("GET",):
            raise ValueError("Only GET method allowed")

        if not self.read_only:
            raise ValueError("API must be read-only")

        if not isinstance(self.params_schema, dict):
            raise ValueError("params_schema must be a dict")
