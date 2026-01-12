import pytest

from core.memory.influence.preference_schema import (
    PreferenceInfluence,
    PreferenceType,
    InfluenceStrength,
)
from core.memory.influence.weighting import (
    compute_influence_weight,
    InfluenceWeight,
    MAX_INFLUENCE_WEIGHT,
    DEFAULT_SOFT_WEIGHT,
)


def test_inactive_influence_returns_none():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.TONE,
        value="friendly",
        strength=InfluenceStrength.NONE,
    )
    assert compute_influence_weight(pref) is None


def test_soft_influence_returns_weight():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.VERBOSITY,
        value="high",
        strength=InfluenceStrength.SOFT,
        confidence=1.0,
    )
    weight = compute_influence_weight(pref)
    assert isinstance(weight, InfluenceWeight)
    assert weight.value <= MAX_INFLUENCE_WEIGHT


def test_weight_respects_confidence():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.FORMAT,
        value="bullets",
        strength=InfluenceStrength.SOFT,
        confidence=0.5,
    )
    weight = compute_influence_weight(pref)
    assert weight.value == round(DEFAULT_SOFT_WEIGHT * 0.5, 2)


def test_weight_never_exceeds_cap():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.LANGUAGE,
        value="en",
        strength=InfluenceStrength.SOFT,
        confidence=10.0,  # extreme confidence
    )
    weight = compute_influence_weight(pref)
    assert weight.value == MAX_INFLUENCE_WEIGHT


def test_invalid_weight_raises_error():
    with pytest.raises(ValueError):
        InfluenceWeight(value=MAX_INFLUENCE_WEIGHT + 0.01)


def test_explain_is_deterministic():
    weight = InfluenceWeight(value=0.2)
    assert weight.explain() == "Influence weight applied: 0.20 (soft cap)"
