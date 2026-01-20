import pytest
from core.actions.action_planner import ActionPlanner
from core.orchestrator.intent_graph import IntentGraph


class DummyIntentA:
    pass


class DummyIntentB:
    pass


def test_action_planner_creates_planned_actions():
    graph = IntentGraph()
    graph.add_sequential([DummyIntentA(), DummyIntentB()])

    planner = ActionPlanner(
        intent_to_action={
            DummyIntentA: "OPEN_APP",
            DummyIntentB: "SEARCH",
        }
    )

    planned = planner.plan(graph)

    assert len(planned) == 2
    assert planned[0].action_spec.action_type == "OPEN_APP"
    assert planned[1].action_spec.action_type == "SEARCH"


def test_action_planner_wires_dependencies():
    graph = IntentGraph()
    graph.add_sequential([DummyIntentA(), DummyIntentB()])

    planner = ActionPlanner(
        intent_to_action={
            DummyIntentA: "OPEN_APP",
            DummyIntentB: "SEARCH",
        }
    )

    planned = planner.plan(graph)

    first, second = planned
    assert second.dependencies == {first}
    assert first.dependencies == set()


def test_action_planner_missing_mapping_raises():
    graph = IntentGraph()
    graph.add_sequential([DummyIntentA()])

    planner = ActionPlanner(intent_to_action={})

    with pytest.raises(ValueError):
        planner.plan(graph)
