from core.emotional_safety.dependency_signals import DependencySignals


def test_signals_not_empty():
    assert len(DependencySignals.all_signals()) > 0
    assert "only me" in DependencySignals.ZERO_TOLERANCE
