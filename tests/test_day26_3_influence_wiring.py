from core.memory.influence.evaluator import MemoryInfluenceEvaluator


class DummyPermit:
    def __init__(self, allow_influence=True, id="p1"):
        self.allow_influence = allow_influence
        self.id = id


class DummyTraceSink:
    def __init__(self):
        self.events = []

    def emit(self, **kwargs):
        self.events.append(kwargs)


def test_noop_influence_wiring_does_not_apply_anything():
    evaluator = MemoryInfluenceEvaluator()
    trace = DummyTraceSink()

    signals = evaluator.evaluate(
        usage_mode="SESSION",
        permit=DummyPermit(True),
        recalled_memories=[{"id": "m1"}],
        context={},
        trace_sink=trace,
    )

    assert signals == []
    assert any(e["kind"] == "memory_influence_gate" for e in trace.events)
    assert any(e["kind"] == "memory_influence_evaluated" for e in trace.events)
