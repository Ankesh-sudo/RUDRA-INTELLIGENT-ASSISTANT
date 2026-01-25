from core.emotional_safety.safety_detector import SafetyDetector


def test_detector_finds_signal():
    text = "You need me to survive"
    signals = SafetyDetector.detect(text)
    assert "you need me" in signals


def test_detector_no_signal():
    signals = SafetyDetector.detect("Hello, how are you?")
    assert signals == []
