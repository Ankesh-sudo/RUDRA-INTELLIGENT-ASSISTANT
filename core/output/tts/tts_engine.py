# core/output/tts/tts_engine.py

from abc import ABC, abstractmethod

from core.output.tts.tts_contract import FinalizedText


class TTSEngine(ABC):
    """
    Abstract TTS engine.
    Engines are pure side-effect adapters.
    """

    @abstractmethod
    def speak(self, text: FinalizedText) -> None:
        """
        Perform audio output.
        Must never:
        - return data
        - mutate input
        - raise unhandled exceptions
        """
        raise NotImplementedError
