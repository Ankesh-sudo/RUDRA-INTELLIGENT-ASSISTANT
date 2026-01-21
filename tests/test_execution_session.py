from core.orchestrator.execution_session import ExecutionSession
from core.orchestrator.execution_state import SessionState, StepState


class DummyActionSpec:
    action_type = "DUMMY"


class DummyPlannedAction:
    def __init__(self, step_id):
        self.step_id = step_id
        self.action_spec = DummyActionSpec()
        self.dependencies = []


class DummyPlannedActions:
    def __init__(self):
        self.actions = [
            DummyPlannedAction("step-1"),
            DummyPlannedAction("step-2"),
        ]


def test_session_initial_state():
    session = ExecutionSession(session_id="test-session")
    assert session.state == SessionState.CREATED
    assert session.steps == []


def test_attach_plan_transitions_state():
    session = ExecutionSession(session_id="test-session")
    plan = DummyPlannedActions()

    session.attach_plan(plan)

    assert session.state == SessionState.PLANNED
    assert len(session.steps) == 2
    assert session.steps[0].state == StepState.PENDING


def test_abort_cancels_pending_steps():
    session = ExecutionSession(session_id="test-session")
    plan = DummyPlannedActions()

    session.attach_plan(plan)
    session.request_abort()

    assert session.state == SessionState.CANCELLED
    for step in session.steps:
        assert step.state == StepState.SKIPPED
