# core/output/tts/tts_adapter.py

from typing import Optional

from core.output.tts.tts_contract import (
    FinalizedText,
    validate_finalized_text,
    TTSContractViolation,
)
from core.output.tts.tts_registry import TTSEngineRegistry, TTSEngineNotFound
from core.output.tts.tts_engine import TTSEngine


class TTSAdapter:
    """
    Single, fail-closed entry point for TTS.
    """

    @staticmethod
    def speak(
        text,
        *,
        engine_name: str = "disabled",
        interrupt: Optional[str] = None,
    ) -> None:
        """
        Perform optional audio output.

        interrupt:
            - None
            - "SOFT"
            - "HARD"
        """

        # HARD interrupt cancels immediately
        if interrupt == "HARD":
            return None

        try:
            finalized: FinalizedText = validate_finalized_text(text)
        except TTSContractViolation:
            # Contract violation → silent no-op
            return None

        # SOFT interrupt cancels before side-effect
        if interrupt == "SOFT":
            return None

        try:
            engine: TTSEngine = TTSEngineRegistry.get(engine_name)
            engine.speak(finalized)
        except (TTSEngineNotFound, Exception):
            # Any engine failure → silent no-op
            return None

        return None
