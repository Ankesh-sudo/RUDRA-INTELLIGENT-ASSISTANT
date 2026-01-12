from core.memory.influence.gate import (
    evaluate_influence_gate,
    InfluenceGateDecision,
)


class DummyPermit:
    def __init__(self, allow_influence: bool, id: str = "p1"):
        self.allow_influence = allow_influence
        self.id = id


def test_gate_denies_when_mode_disabled():
    result = evaluate_influence_gate(
        usage_mode="DISABLED",
        permit=DummyPermit(True),
        recalled_memories=[{"id": "m1"}],
    )
    assert result.decision == InfluenceGateDecision.DENY
    assert "DISABLED" in result.reason


def test_gate_denies_without_permit():
    result = evaluate_influence_gate(
        usage_mode="SESSION",
        permit=None,
        recalled_memories=[{"id": "m1"}],
    )
    assert result.decision == InfluenceGateDecision.DENY


def test_gate_denies_when_permit_disallows_influence():
    result = evaluate_influence_gate(
        usage_mode="SESSION",
        permit=DummyPermit(False),
        recalled_memories=[{"id": "m1"}],
    )
    assert result.decision == InfluenceGateDecision.DENY


def test_gate_denies_when_no_recalled_memories():
    result = evaluate_influence_gate(
        usage_mode="SESSION",
        permit=DummyPermit(True),
        recalled_memories=[],
    )
    assert result.decision == InfluenceGateDecision.DENY


def test_gate_allows_when_all_conditions_met():
    result = evaluate_influence_gate(
        usage_mode="SESSION",
        permit=DummyPermit(True),
        recalled_memories=[{"id": "m1"}],
    )
    assert result.decision == InfluenceGateDecision.ALLOW
    assert result.permit_id == "p1"
