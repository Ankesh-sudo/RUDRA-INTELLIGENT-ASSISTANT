from dataclasses import dataclass
from typing import Any, Dict, Set

from core.os.executor.executor_contract import ExecutorContract
from core.os.executor.dry_run_backend import DryRunBackend
from core.os.explain.explain_surface import ExplainSurface
from core.os.permission.consent_store import ConsentStore
from core.os.permission.permission_evaluator import PermissionEvaluator

# Day 50: Linux live backends (LOW RISK ONLY)
from core.os.linux.app_control import AppControl
from core.os.linux.system_info import SystemInfo


@dataclass(frozen=True)
class ExecutionPlan:
    action_type: str
    target: str
    parameters: Dict[str, Any]
    risk_level: str
    required_scopes: Set[str]
    explanation: Dict[str, Any]
    dry_run: bool


class GuardedExecutor(ExecutorContract):
    """
    Central authority gate for OS actions.

    Day 50:
    - Permission enforced
    - Consent gated
    - LOW-RISK real execution enabled
    - Persona completely blocked
    """

    def __init__(self):
        self._backend = DryRunBackend()  # still used for denied / confirm paths
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

        # 5. Permission granted → controlled live execution (LOW RISK ONLY)
        result = None

        if action_spec.action_type == "OPEN_APP":
            result = AppControl.open_app(
                action_spec.parameters["app_name"]
            )

        elif action_spec.action_type == "SYSTEM_INFO":
            result = SystemInfo.uname()

        else:
            # Any non-whitelisted action is still blocked
            result = {
                "ok": False,
                "error": "Action not enabled for live execution",
            }

        return ExecutionPlan(
            action_type=action_spec.action_type,
            target=action_spec.target,
            parameters=action_spec.parameters,
            risk_level=action_spec.risk_level,
            required_scopes=set(action_spec.required_scopes),
            explanation={
                **explanation,
                "permission": "GRANTED",
                "result": result,
            },
            dry_run=False,
        )
