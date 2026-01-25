from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    """
    Immutable user claim.
    Must be explicit and declarative.
    """
    text: str

    def validate(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("Claim cannot be empty")

        if self.text.strip().endswith("?"):
            raise ValueError("Claim must be declarative, not a question")

        if len(self.text.strip()) < 5:
            raise ValueError("Claim too short to evaluate")
