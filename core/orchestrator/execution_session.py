from typing import List, Optional, Tuple
import uuid

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
    - Observation-safe (read-only)
    """

    def __init__(self, session_id: Optional[str] = None, working_memory=None):
        # DAY 69 — default-safe session id
        self.session_id = session_id or f"session-{uuid.uuid4().hex[:8]}"
        self.state = SessionState.CREATED
        self.steps: List[ExecutionStep] = []
        self.context = SessionContext(working_memory) if working_memory else None
        self.abort_requested = False

        # Observation sink (read-only)
        self._observations: List[Tuple[str, str]] = []

        # -----------------------------
        # STEP 6 — Explain storage (read-only)
        # -----------------------------
        self._last_explain_surface = None

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
    # DAY 69 — Observation handling
    # -----------------------------

    def attach_observation(self, kind: str, value: str) -> None:
        """
        Attach a read-only observation to the session.
        """
        self._observations.append((kind, value))

    def observations(self) -> List[Tuple[str, str]]:
        return list(self._observations)

    # -----------------------------
    # STEP 6 — Explain surface handling
    # -----------------------------

    def set_explain_surface(self, explain_surface) -> None:
        """
        Store the final ExplainSurface for this session.

        Rules:
        - Stored once per completed decision
        - Read-only thereafter
        - No recomputation
        """
        self._last_explain_surface = explain_surface

    def get_last_explain_surface(self):
        """
        Retrieve the last stored ExplainSurface (if any).
        """
        return self._last_explain_surface

    # -----------------------------
    # Introspection / Explain-safe snapshot
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
            "observations": [
                {"type": kind, "value": value}
                for kind, value in self._observations
            ],
            "has_explain_surface": self._last_explain_surface is not None,
        }
