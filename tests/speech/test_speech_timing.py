import time
from core.speech.speech_timing import SpeechTiming


def test_speech_timing_waits_minimum_delay():
    timing = SpeechTiming(min_delay_sec=0.05)
    start = time.time()
    timing.wait()
    elapsed = time.time() - start

    assert elapsed >= 0.05
