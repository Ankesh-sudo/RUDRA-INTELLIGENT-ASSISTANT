from dataclasses import dataclass
from typing import Any, Dict

from core.os.executor.executor_contract import ExecutorContract
from core.os.executor.dry_run_backend import DryRunBackend
from core.os.explain.explain_surface import ExplainSurface


@dataclass(frozen=True)
class ExecutionPlan:
    action_type: str
    target: str
    parameters: Dict[str, Any]
    risk_level: str
    required_scopes: set
    explanation: Dict[str, Any]
    dry_run: bool = True


class GuardedExecutor(ExecutorContract):
    """
    Central authority gate for OS actions.
    Day 48: dry-run only.
    """

    def __init__(self):
        self._backend = DryRunBackend()

    def execute(self, action_spec):
        if action_spec is None:
            raise ValueError("ActionSpec is required")

        explanation = ExplainSurface.explain(action_spec)

        # backend is called but does nothing real
        self._backend.run()

        return ExecutionPlan(
            action_type=action_spec.action_type,
            target=action_spec.target,
            parameters=action_spec.parameters,
            risk_level=action_spec.risk_level,
            required_scopes=set(action_spec.required_scopes),
            explanation=explanation,
            dry_run=True,
        )
