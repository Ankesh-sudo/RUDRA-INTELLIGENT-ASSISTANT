from typing import Dict, Callable

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_engine_noop import NoOpTTSEngine
from core.output.tts.engines.espeak_engine import EspeakEngine

# Day 41: Coqui engine is registered but NOT ACTIVE
# Import is safe because engine is a pure stub (no audio, no models)
from core.output.tts.engines.coqui_engine import CoquiTTSEngine

# Day 41: Google Cloud TTS (TEMPORARY PRODUCTION BACKEND)
# IMPORTANT: Engine must NOT initialize at import time
from core.output.tts.engines.google_tts_engine import GoogleTTSEngine


class TTSEngineNotFound(Exception):
    """Raised when a requested TTS engine is not registered."""
    pass


class TTSEngineRegistry:
    """
    Explicit, deterministic TTS engine registry (LAZY).

    Architectural guarantees:
    - NO engine is instantiated at import time
    - Engines are side-effect only
    - Default engine is NOOP
    - Google TTS is TEMPORARY and replaceable
    - Safe for pytest collection without credentials
    """

    _ENGINES: Dict[str, Callable[[], TTSEngine]] = {
        # 🔇 SAFE DEFAULTS
        "disabled": lambda: NoOpTTSEngine(),
        "noop": lambda: NoOpTTSEngine(),

        # 🧪 LEGACY / TEST VOICE
        "kakora": lambda: EspeakEngine("hi"),

        # 🟣 REAL VOICE PIPELINE (LOCKED — DAY 41)
        # Must remain inactive unless explicitly used
        "coqui": lambda: CoquiTTSEngine(),

        # 🔵 TEMPORARY PRODUCTION (GOOGLE CLOUD TTS)
        # Client is created ONLY when engine is requested
        "google_hi_male": lambda: GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Standard-B",
        ),
        "google_hi_female": lambda: GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Standard-A",
        ),
    }

    @classmethod
    def get(cls, name: str) -> TTSEngine:
        if not isinstance(name, str):
            raise TTSEngineNotFound("Engine name must be a string")

        factory = cls._ENGINES.get(name)

        if factory is None:
            raise TTSEngineNotFound(f"TTS engine not found: {name}")

        # Engine is instantiated HERE — never earlier
        return factory()
