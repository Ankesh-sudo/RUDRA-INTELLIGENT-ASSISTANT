from typing import Dict

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_engine_noop import NoOpTTSEngine
from core.output.tts.engines.espeak_engine import EspeakEngine


class TTSEngineNotFound(Exception):
    """Raised when a requested TTS engine is not registered."""
    pass


class TTSEngineRegistry:
    """
    Explicit, deterministic TTS engine registry.
    """

    _ENGINES: Dict[str, TTSEngine] = {
        "disabled": NoOpTTSEngine(),
        "noop": NoOpTTSEngine(),

        # REAL VOICE (GUARANTEED, PRE–DAY 40)
        "kakora": EspeakEngine("hi"),
    }

    @classmethod
    def get(cls, name: str) -> TTSEngine:
        if not isinstance(name, str):
            raise TTSEngineNotFound("Engine name must be a string")

        engine = cls._ENGINES.get(name)

        if engine is None:
            raise TTSEngineNotFound(f"TTS engine not found: {name}")

        return engine
