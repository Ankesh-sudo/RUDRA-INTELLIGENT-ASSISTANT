from dataclasses import dataclass


@dataclass(frozen=True)
class Premise:
    """
    Atomic supporting statement.
    """
    text: str

    def validate(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("Premise cannot be empty")

        banned = ["feel", "believe", "think", "emotion"]
        for word in banned:
            if word in self.text.lower():
                raise ValueError("Premise contains emotional language")
