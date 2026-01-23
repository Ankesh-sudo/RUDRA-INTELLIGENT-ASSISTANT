from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceRoute:
    persona: str
    engine_key: str


# 🔒 DAY 45 — VOICE ROUTING CONTRACT (LOCKED)
# Persona voices are FIXED and NON-SYMBOLIC.
# No aliases, no dynamic resolution, no runtime mutation.

MAAHI_VOICE_ROUTE = VoiceRoute(
    persona="maahi",
    engine_key="google_hi_female",
)

RUDRA_VOICE_ROUTE = VoiceRoute(
    persona="rudra",
    engine_key="google_hi_male",
)


# 🔐 Canonical persona → engine map (read-only)
PERSONA_VOICE_MAP = {
    "maahi": MAAHI_VOICE_ROUTE.engine_key,
    "rudra": RUDRA_VOICE_ROUTE.engine_key,
}
