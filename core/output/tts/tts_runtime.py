from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Optional

from core.output.tts.tts_adapter import TTSAdapter


class TTSRuntime:
    """
    Executes TTS safely:
    - Non-blocking
    - Time-bounded
    - Fail-closed
    """

    _EXECUTOR = ThreadPoolExecutor(max_workers=1)
    _TIMEOUT_SECONDS = 2.5  # conservative, configurable later

    @classmethod
    def speak(
        cls,
        finalized_text,
        *,
        engine_name: str,
        interrupt: Optional[str] = None,
    ) -> None:
        # HARD interrupt: do nothing
        if interrupt == "HARD":
            return None

        future = cls._EXECUTOR.submit(
            TTSAdapter.speak,
            finalized_text,
            engine_name=engine_name,
            interrupt=interrupt,
        )

        try:
            future.result(timeout=cls._TIMEOUT_SECONDS)
        except TimeoutError:
            # Timeout → abandon silently
            return None
        except Exception:
            # Any failure → silent no-op
            return None

        return None
