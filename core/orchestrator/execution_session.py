from typing import List, Optional

from .execution_state import SessionState, StepState
from .session_context import SessionContext


class ExecutionStep:
    """
    Immutable execution step derived from PlannedAction.
    """

    def __init__(
        self,
        step_id: str,
        action_spec,
        dependencies: Optional[List[str]] = None,
    ):
        self.step_id = step_id
        self.action_spec = action_spec
        self.dependencies = dependencies or []
        self.state = StepState.PENDING
        self.error = None

    def mark_ready(self):
        self.state = StepState.READY

    def mark_running(self):
        self.state = StepState.RUNNING

    def mark_done(self):
        self.state = StepState.DONE

    def mark_failed(self, error: str):
        self.state = StepState.FAILED
        self.error = error

    def skip(self, reason: str):
        self.state = StepState.SKIPPED
        self.error = reason


class ExecutionSession:
    """
    Single authoritative execution boundary.

    Rules:
    - Owns exactly one user command
    - No execution happens here
    - No permission evaluation
    - No OS calls
    """

    def __init__(self, session_id: str, working_memory=None):
        self.session_id = session_id
        self.state = SessionState.CREATED
        self.steps: List[ExecutionStep] = []
        self.context = SessionContext(working_memory) if working_memory else None
        self.abort_requested = False

    # -----------------------------
    # Planning attachment
    # -----------------------------

    def attach_plan(self, planned_actions):
        """
        Converts PlannedActions → ExecutionSteps.
        """
        if self.state is not SessionState.CREATED:
            raise RuntimeError("Plan can only be attached once, from CREATED state")

        self.steps = self._build_steps(planned_actions)
        self.state = SessionState.PLANNED

    def _build_steps(self, planned_actions) -> List[ExecutionStep]:
        """
        Deterministic conversion.
        No execution, no validation beyond structure.
        """
        steps = []

        for pa in planned_actions.actions:
            step = ExecutionStep(
                step_id=pa.step_id,
                action_spec=pa.action_spec,
                dependencies=list(pa.dependencies),
            )
            steps.append(step)

        return steps

    # -----------------------------
    # Control hooks
    # -----------------------------

    def request_abort(self):
        """
        External cancel / interrupt hook.
        """
        self.abort_requested = True
        self.state = SessionState.CANCELLED

        for step in self.steps:
            if step.state in {StepState.PENDING, StepState.READY}:
                step.skip("session_cancelled")

    # -----------------------------
    # Introspection / Explain
    # -----------------------------

    def summary(self) -> dict:
        """
        Explain-safe snapshot.
        """
        return {
            "session_id": self.session_id,
            "state": self.state.name,
            "steps": [
                {
                    "step_id": step.step_id,
                    "action_type": getattr(
                        step.action_spec, "action_type", None
                    ),
                    "state": step.state.name,
                    "dependencies": list(step.dependencies),
                    "error": step.error,
                }
                for step in self.steps
            ],
        }
