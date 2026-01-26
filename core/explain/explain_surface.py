from typing import List, Dict, Any, Union

from core.explain.formatter import format_section


class ExplainSurface:
    """
    Immutable, user-facing explanation payload.

    Rules:
    - Factual only
    - No persuasion
    - No persona logic
    - No side effects
    - Safe to log / replay
    """

    def __init__(self, lines: List[str]):
        if not lines:
            raise ValueError("ExplainSurface requires at least one line")

        self._lines = list(lines)

    # -------------------------------------------------
    # Construction helpers (OBJECT)
    # -------------------------------------------------

    @classmethod
    def from_lines(cls, *lines: str) -> "ExplainSurface":
        cleaned = [line for line in lines if line is not None]
        return cls(cleaned)

    @classmethod
    def single(cls, line: str) -> "ExplainSurface":
        return cls([line])

    # -------------------------------------------------
    # STEP 4 — FORMATTED RESPONSE CONSTRUCTORS
    # -------------------------------------------------

    @classmethod
    def from_knowledge(
        cls,
        payload: Union[str, Dict[str, Any]],
    ) -> "ExplainSurface":
        """
        Accepts:
        - str  → already formatted knowledge text (CURRENT SYSTEM)
        - dict → structured knowledge payload (FUTURE SYSTEM)

        Dict payload shape:
        {
            "topic": str,
            "answer": str,
            "citation": Optional[str]
        }
        """

        # ✅ CURRENT SYSTEM (string payload)
        if isinstance(payload, str):
            return cls(payload.splitlines())

        # ✅ FUTURE SYSTEM (structured payload)
        text = format_section(
            title=payload.get("topic", "Knowledge").title(),
            body=payload.get("answer", ""),
            footer=(
                f"Source: {payload['citation']}"
                if payload.get("citation")
                else None
            ),
        )
        return cls(text.splitlines())

    @classmethod
    def from_action(cls, message: str) -> "ExplainSurface":
        """
        Action explanations remain simple in Step 4.
        """
        return cls.single(message)

    # -------------------------------------------------
    # Day 55 — RESPONSE HELPERS (DICT PAYLOADS)
    # -------------------------------------------------

    @staticmethod
    def info(
        message: str,
        payload: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return {
            "type": "info",
            "message": message,
            "payload": payload,
        }

    @staticmethod
    def deny(message: str) -> Dict[str, Any]:
        return {
            "type": "deny",
            "message": message,
        }

    @staticmethod
    def noop(message: str) -> Dict[str, Any]:
        return {
            "type": "noop",
            "message": message,
        }

    @staticmethod
    def error(message: str) -> Dict[str, Any]:
        return {
            "type": "error",
            "message": message,
        }

    @staticmethod
    def permission_denied(permission: str) -> Dict[str, Any]:
        return {
            "type": "permission_denied",
            "permission": permission,
        }

    # -------------------------------------------------
    # Accessors
    # -------------------------------------------------

    @property
    def lines(self) -> List[str]:
        return list(self._lines)

    def as_text(self) -> str:
        """
        Plain text rendering.
        """
        return "\n".join(self._lines)

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __str__(self) -> str:
        return self.as_text()

    def __repr__(self) -> str:
        return f"ExplainSurface(lines={self._lines!r})"
