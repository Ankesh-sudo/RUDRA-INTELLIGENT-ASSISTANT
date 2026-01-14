from typing import Optional
from core.output.tts.voice_routing import MAAHI_VOICE_ROUTE
from core.output.tts.tts_adapter import TTSAdapter

def dispatch_tts(
    finalized_text,
    *,
    persona: Optional[str],
    interrupt: Optional[str] = None,
) -> None:
    if persona == MAAHI_VOICE_ROUTE.persona:
        TTSAdapter.speak(
            finalized_text,
            engine_name=MAAHI_VOICE_ROUTE.engine_key,
            interrupt=interrupt,
        )
        return

    TTSAdapter.speak(
        finalized_text,
        engine_name="disabled",
        interrupt=interrupt,
    )
