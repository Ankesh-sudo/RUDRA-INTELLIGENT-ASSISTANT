# core/output/tts/tts_engine.py

from abc import ABC, abstractmethod

from core.response.final_envelope import FinalResponseEnvelope


class TTSEngine(ABC):
    """
    Abstract TTS engine (Day 37 locked).

    Invariants:
    - Voice is transport only
    - TTS consumes FINAL text only
    - No persona, intent, memory, or preference access
    - No mutation, no return value, no authority
    """

    @abstractmethod
    def speak(self, envelope: FinalResponseEnvelope) -> None:
        """
        Perform audio output.

        The envelope is immutable and already persona-applied.

        TTS engines MUST:
        - Read envelope.final_text only
        - Respect envelope.tts_allowed
        - Produce side effects only (audio)

        TTS engines MUST NEVER:
        - Modify text
        - Inject emotion, fillers, or phrasing
        - Access persona profile or fingerprint
        - Return data
        - Raise unhandled exceptions
        """
        raise NotImplementedError
