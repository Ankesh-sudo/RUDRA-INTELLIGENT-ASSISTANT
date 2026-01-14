from dataclasses import dataclass

@dataclass(frozen=True)
class VoiceRoute:
    persona: str
    engine_key: str

MAAHI_VOICE_ROUTE = VoiceRoute(
    persona="maahi",
    engine_key="google_hi_female",
)
