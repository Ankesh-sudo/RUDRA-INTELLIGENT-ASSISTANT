from core.metrics.latency_timer import LatencyTimer


def test_latency_timer_measures_time():
    timer = LatencyTimer()
    with timer.measure() as elapsed:
        pass
    assert elapsed() >= 0.0
