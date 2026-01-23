from typing import Dict, Callable, Union

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_engine_noop import NoOpTTSEngine
from core.output.tts.engines.espeak_engine import EspeakEngine

# Day 41: Coqui engine is registered but NOT ACTIVE
from core.output.tts.engines.coqui_engine import CoquiTTSEngine

# Day 41+: Google Cloud TTS (TEMPORARY PRODUCTION BACKEND)
# IMPORTANT: Engine must NOT initialize at import time
from core.output.tts.engines.google_tts_engine import GoogleTTSEngine


class TTSEngineNotFound(Exception):
    """Raised when a requested TTS engine is not registered."""
    pass


class TTSEngineRegistry:
    """
    Explicit, deterministic TTS engine registry (LAZY + TEST-SAFE).

    Architectural guarantees:
    - NO engine is instantiated at import time
    - Engines are side-effect only
    - Default engine is NOOP
    - Google TTS is TEMPORARY and replaceable
    - Safe for pytest collection without credentials
    - Supports test injection of engine instances
    """

    # NOTE:
    # Values may be:
    #   - Callable[[], TTSEngine]  (production)
    #   - TTSEngine instance       (tests / monkeypatching)
    _ENGINES: Dict[str, Union[Callable[[], TTSEngine], TTSEngine]] = {
        # -------------------------------------------------
        # 🔇 SAFE DEFAULTS
        # -------------------------------------------------
        "disabled": lambda: NoOpTTSEngine(),
        "noop": lambda: NoOpTTSEngine(),

        # -------------------------------------------------
        # 🧪 LEGACY / TEST VOICE
        # -------------------------------------------------
        "kakora": lambda: EspeakEngine("hi"),

        # -------------------------------------------------
        # 🟣 OFFLINE PIPELINE (LOCKED — DAY 41)
        # -------------------------------------------------
        "coqui": lambda: CoquiTTSEngine(),

        # -------------------------------------------------
        # 🔵 GOOGLE CLOUD TTS (TEMPORARY PRODUCTION BACKEND)
        # -------------------------------------------------

        # Low-level explicit voices
        "google_hi_male": lambda: GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Wavenet-D",
        ),
        "google_hi_female": lambda: GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Wavenet-C",
        ),

        # -------------------------------------------------
        # 👤 PERSONA-BOUND ALIASES (READABLE, STABLE)
        # -------------------------------------------------
        # These are the keys used by voice_routing.py
        "google_rudra": lambda: GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Wavenet-D",
        ),
        "google_maahi": lambda: GoogleTTSEngine(
            language_code="hi-IN",
            voice_name="hi-IN-Wavenet-C",
        ),
    }

    @classmethod
    def get(cls, name: str) -> TTSEngine:
        if not isinstance(name, str):
            raise TTSEngineNotFound("Engine name must be a string")

        entry = cls._ENGINES.get(name)

        if entry is None:
            raise TTSEngineNotFound(f"TTS engine not found: {name}")

        # ✅ SUPPORT BOTH:
        # - Lazy factories (callable)
        # - Direct engine instances (tests)
        if callable(entry):
            return entry()

        return entry
