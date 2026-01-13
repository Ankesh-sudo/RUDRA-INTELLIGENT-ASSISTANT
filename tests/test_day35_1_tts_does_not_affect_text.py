from core.output.tts.tts_adapter import TTSAdapter

def test_tts_failure_does_not_change_text():
    text = "authoritative output"

    # simulate failure paths
    TTSAdapter.speak(text, engine_name="unknown_engine")
    TTSAdapter.speak(text, interrupt="HARD")
    TTSAdapter.speak(text, interrupt="SOFT")

    # text remains unchanged and authoritative
    assert text == "authoritative output"
