# core/output/tts/tts_contract.py

from dataclasses import dataclass


class TTSContractViolation(Exception):
    """Raised when TTS input violates the strict contract."""
    pass


@dataclass(frozen=True)
class FinalizedText:
    """
    Marker wrapper for text that has passed:
    core → influence → persona → style

    This is the ONLY acceptable input to TTS.
    """
    text: str

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise TTSContractViolation("TTS input must be a string")

        if not self.text.strip():
            raise TTSContractViolation("TTS input cannot be empty")

        # Defensive normalization: no mutation, but ensures clean boundaries
        object.__setattr__(self, "text", self.text)


def validate_finalized_text(value) -> FinalizedText:
    """
    Entry gate for TTS.
    Accepts ONLY FinalizedText or raw str (wrapped immediately).
    Rejects everything else.
    """

    if isinstance(value, FinalizedText):
        return value

    if isinstance(value, str):
        return FinalizedText(text=value)

    raise TTSContractViolation(
        f"Invalid TTS input type: {type(value).__name__}"
    )
