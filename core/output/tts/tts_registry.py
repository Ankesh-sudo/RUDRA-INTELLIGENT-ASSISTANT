from typing import Dict

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_engine_noop import NoOpTTSEngine
from core.output.tts.engines.espeak_engine import EspeakEngine

# Day 41: Coqui engine is registered but NOT ACTIVE
# Import is safe because engine is a pure stub (no audio, no models)
from core.output.tts.engines.coqui_engine import CoquiTTSEngine

# Day 41: Google Cloud TTS (TEMPORARY PRODUCTION BACKEND)
# Cloud-based, final-text-only, side-effect adapter
from core.output.tts.engines.google_tts_engine import GoogleTTSEngine


class TTSEngineNotFound(Exception):
    """Raised when a requested TTS engine is not registered."""
    pass


class TTSEngineRegistry:
    """
    Explicit, deterministic TTS engine registry.

    Architectural guarantees:
    - Engines are side-effect only
    - Default engine is NOOP
    - No runtime audio before Day 48 (unless explicitly configured)
    - Coqui exists but is locked until explicitly enabled
    - Google TTS is TEMPORARY and replaceable
    """

    _ENGINES: Dict[str, TTSEngine] = {
        # 🔇 SAFE DEFAULTS
        "disabled": NoOpTTSEngine(),
        "noop": NoOpTTSEngine(),

        # 🧪 LEGACY / TEST VOICE (PRE–DAY 40 ONLY)
        "kakora": EspeakEngine("hi"),

        # 🟣 REAL VOICE PIPELINE (LOCKED — DAY 41)
        # Do NOT enable before Day 48
        "coqui": CoquiTTSEngine(),

        # 🔵 TEMPORARY PRODUCTION (GOOGLE CLOUD TTS)
        # Safe, final-text-only, no logic influence
        "google_hi_male": GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Standard-B",
        ),
        "google_hi_female": GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Standard-A",
        ),
    }

    @classmethod
    def get(cls, name: str) -> TTSEngine:
        if not isinstance(name, str):
            raise TTSEngineNotFound("Engine name must be a string")

        engine = cls._ENGINES.get(name)

        if engine is None:
            raise TTSEngineNotFound(f"TTS engine not found: {name}")

        return engine
