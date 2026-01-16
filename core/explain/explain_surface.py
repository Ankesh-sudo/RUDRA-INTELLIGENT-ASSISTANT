from typing import List


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
    # Construction helpers
    # -------------------------------------------------

    @classmethod
    def from_lines(cls, *lines: str) -> "ExplainSurface":
        cleaned = [line for line in lines if line is not None]
        return cls(cleaned)

    @classmethod
    def single(cls, line: str) -> "ExplainSurface":
        return cls([line])

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
