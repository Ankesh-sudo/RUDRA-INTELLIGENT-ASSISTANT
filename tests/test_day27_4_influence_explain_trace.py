from core.memory.influence.explain_trace import build_influence_explain_trace
from core.memory.influence.preference_schema import (
    PreferenceInfluence,
    PreferenceType,
    InfluenceStrength,
)
from core.memory.influence.weighting import InfluenceWeight


def test_empty_inputs_return_empty_trace():
    trace = build_influence_explain_trace(
        influences=[],
        weight=None,
        phrasing_explanations=[],
    )
    assert trace == []


def test_active_preferences_are_included():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.TONE,
        value="formal",
        strength=InfluenceStrength.SOFT,
    )
    trace = build_influence_explain_trace(
        influences=[pref],
        weight=None,
        phrasing_explanations=[],
    )
    assert len(trace) == 1
    assert "Preference influence detected" in trace[0]


def test_inactive_preferences_are_excluded():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.TONE,
        value="formal",
        strength=InfluenceStrength.NONE,
    )
    trace = build_influence_explain_trace(
        influences=[pref],
        weight=None,
        phrasing_explanations=[],
    )
    assert trace == []


def test_weight_is_included_when_present():
    weight = InfluenceWeight(value=0.2)
    trace = build_influence_explain_trace(
        influences=[],
        weight=weight,
        phrasing_explanations=[],
    )
    assert trace == [weight.explain()]


def test_phrasing_explanations_are_appended():
    phrasing_explanations = [
        "Preference influence detected: tone = 'formal' (strength=soft, source=memory)",
        "Influence weight applied: 0.20 (soft cap)",
    ]
    trace = build_influence_explain_trace(
        influences=[],
        weight=None,
        phrasing_explanations=phrasing_explanations,
    )
    assert trace == phrasing_explanations


def test_deterministic_order_preserved():
    pref = PreferenceInfluence(
        pref_type=PreferenceType.VERBOSITY,
        value="low",
        strength=InfluenceStrength.SOFT,
    )
    weight = InfluenceWeight(value=0.2)
    phrasing_explanations = ["Applied verbosity reduction"]

    trace = build_influence_explain_trace(
        influences=[pref],
        weight=weight,
        phrasing_explanations=phrasing_explanations,
    )

    assert trace == [
        pref.explain(),
        weight.explain(),
        "Applied verbosity reduction",
    ]
