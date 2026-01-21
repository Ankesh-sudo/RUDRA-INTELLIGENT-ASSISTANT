from core.orchestrator.execution_state import SessionState, StepState
from core.os.executor.guarded_executor import GuardedExecutor
from core.control.global_interrupt import InterruptType


class SessionExecutor:
    """
    Day 60 — Guarded Session Execution

    Responsibilities:
    - Execute a single ExecutionSession step-by-step
    - Bridge ExecutionSession → GuardedExecutor
    - Respect interrupts, dry-run vs live execution
    - Populate ExplainSurface
    """

    def __init__(self, session, interrupt_controller):
        self.session = session
        self.interrupt_controller = interrupt_controller

    def execute(self):
        """
        Execute the session sequentially.

        HARD RULES:
        - No permission checks here
        - No OS calls here
        - No parallel execution
        - No dependency logic (Day 62+)
        """

        if self.session.state != SessionState.READY:
            raise RuntimeError(
                f"Session must be READY, got {self.session.state.name}"
            )

        self.session.state = SessionState.RUNNING

        for index, step in enumerate(self.session.steps):
            # ----------------------------------
            # HARD interrupt check (global)
            # ----------------------------------
            if self.interrupt_controller.is_triggered(InterruptType.HARD):
                self._abort_session("hard_interrupt")
                return self._finalize()

            # ----------------------------------
            # Step lifecycle: RUNNING
            # ----------------------------------
            step.state = StepState.RUNNING

            # ----------------------------------
            # Explain: step start
            # ----------------------------------
            self.session.explain_surface.add_step(
                step_index=index,
                action_name=step.planned_action.action_name,
                dry_run=self.session.context.dry_run,
            )

            try:
                GuardedExecutor.execute(
                    planned_action=step.planned_action,
                    dry_run=self.session.context.dry_run,
                    interrupt_controller=self.interrupt_controller,
                    explain_surface=self.session.explain_surface,
                )

                step.state = StepState.DONE

            except Exception as exc:
                step.state = StepState.FAILED
                step.error = str(exc)

                self.session.state = SessionState.FAILED

                self.session.explain_surface.mark_failed(
                    step_index=index,
                    reason=str(exc),
                )

                return self._finalize()

        # ----------------------------------
        # Session completed successfully
        # ----------------------------------
        self.session.state = SessionState.COMPLETED
        return self._finalize()

    # -------------------------------------------------
    # Internal helpers
    # -------------------------------------------------

    def _abort_session(self, reason: str):
        self.session.state = SessionState.CANCELLED
        self.session.explain_surface.mark_cancelled(reason)

    def _finalize(self):
        """
        Final session summary.
        No execution, no mutation beyond this point.
        """

        return {
            "session_id": self.session.session_id,
            "state": self.session.state.name,
            "steps": [
                {
                    "step_id": step.step_id,
                    "state": step.state.name,
                    "error": step.error,
                }
                for step in self.session.steps
            ],
            "explain": self.session.explain_surface.render(),
        }
