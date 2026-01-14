from dataclasses import dataclass
from typing import Any, Dict, Set

from core.os.executor.executor_contract import ExecutorContract
from core.os.executor.dry_run_backend import DryRunBackend
from core.os.explain.explain_surface import ExplainSurface
from core.os.permission.consent_store import ConsentStore
from core.os.permission.permission_evaluator import PermissionEvaluator


@dataclass(frozen=True)
class ExecutionPlan:
    action_type: str
    target: str
    parameters: Dict[str, Any]
    risk_level: str
    required_scopes: Set[str]
    explanation: Dict[str, Any]
    dry_run: bool = True


class GuardedExecutor(ExecutorContract):
    """
    Central authority gate for OS actions.

    Day 49:
    - Permission enforced
    - Consent gated
    - Dry-run only
    - Persona completely blocked
    """

    def __init__(self):
        self._backend = DryRunBackend()
        self._consent_store = ConsentStore()
        self._permission_evaluator = PermissionEvaluator(self._consent_store)

    def execute(self, action_spec):
        if action_spec is None:
            raise ValueError("ActionSpec is required")

        # 1. Permission evaluation (authoritative)
        decision = self._permission_evaluator.evaluate(action_spec)

        # 2. Base explanation (what / why / risk)
        explanation = ExplainSurface.explain(action_spec)

        # 3. Permission denied
        if not decision.allowed:
            return ExecutionPlan(
                action_type=action_spec.action_type,
                target=action_spec.target,
                parameters=action_spec.parameters,
                risk_level=action_spec.risk_level,
                required_scopes=set(action_spec.required_scopes),
                explanation={
                    **explanation,
                    "permission": "DENIED",
                    "prompt": decision.prompt_payload,
                },
                dry_run=True,
            )

        # 4. Confirmation required (high risk or first-time)
        if decision.requires_confirmation:
            return ExecutionPlan(
                action_type=action_spec.action_type,
                target=action_spec.target,
                parameters=action_spec.parameters,
                risk_level=action_spec.risk_level,
                required_scopes=set(action_spec.required_scopes),
                explanation={
                    **explanation,
                    "permission": "CONFIRMATION_REQUIRED",
                    "prompt": decision.prompt_payload,
                },
                dry_run=True,
            )

        # 5. Permission granted → still dry-run only
        self._backend.run()

        return ExecutionPlan(
            action_type=action_spec.action_type,
            target=action_spec.target,
            parameters=action_spec.parameters,
            risk_level=action_spec.risk_level,
            required_scopes=set(action_spec.required_scopes),
            explanation={
                **explanation,
                "permission": "GRANTED",
            },
            dry_run=True,
        )
