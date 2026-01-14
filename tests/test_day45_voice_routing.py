from core.output.tts.voice_routing import MAAHI_VOICE_ROUTE

def test_maahi_voice_is_fixed():
    assert MAAHI_VOICE_ROUTE.engine_key == "google_hi_female"
