from dataclasses import dataclass
from typing import Any, Dict, Set

from core.os.executor.executor_contract import ExecutorContract
from core.os.executor.dry_run_backend import DryRunBackend
from core.os.executor.os_control_stub import OSControlStubExecutor
from core.os.permission.consent_store import ConsentStore
from core.os.permission.permission_evaluator import PermissionEvaluator

from core.os.linux.app_control import AppControl
from core.os.linux.system_info import SystemInfo


# --------------------------------------------------
# EXECUTION PLAN (LOCKED)
# --------------------------------------------------

@dataclass(frozen=True)
class ExecutionPlan:
    action_type: str
    target: str
    parameters: Dict[str, Any]
    risk_level: str
    required_scopes: Set[str]
    explanation: Dict[str, Any]
    dry_run: bool


# --------------------------------------------------
# GUARDED EXECUTOR
# --------------------------------------------------

class GuardedExecutor(ExecutorContract):
    """
    Central authority gate for OS actions.

    Day 50:
    - Permission enforced
    - Consent gated
    - LOW-RISK real execution enabled
    - Persona completely blocked

    Day 61:
    - OS_CONTROL actions routed to stub only
    - No real OS mutations
    """

    def __init__(self):
        self._backend = DryRunBackend()
        self._consent_store = ConsentStore()
        self._permission_evaluator = PermissionEvaluator(self._consent_store)

    def execute(self, action_spec):
        if action_spec is None:
            raise ValueError("ActionSpec is required")

        # --------------------------------------------------
        # DAY 61 — OS CONTROL (STUB ONLY, SEALED)
        # --------------------------------------------------
        if action_spec.category == "OS_CONTROL":
            OSControlStubExecutor.execute(action_spec)

            return ExecutionPlan(
                action_type=action_spec.action_type,
                target=action_spec.target,
                parameters=action_spec.parameters,
                risk_level=action_spec.risk_level,
                required_scopes=set(action_spec.required_scopes),
                explanation={
                    "status": "not_implemented",
                    "message": (
                        f"OS control capability '{action_spec.capability}' "
                        "is declared but not executable yet."
                    ),
                    "what": "OS control action blocked",
                    "why": "OS control is explicitly disabled at this stage",
                    "risk_level": action_spec.risk_level,
                    "permission": "DENIED",
                    "details": {
                        # ✅ ENUM OBJECT — REQUIRED BY TEST
                        "capability": action_spec.capability,
                        "parameters": action_spec.parameters or {},
                    },
                },
                dry_run=True,
            )

        # --------------------------------------------------
        # DAY 48–50 FLOW (LOCKED)
        # --------------------------------------------------

        decision = self._permission_evaluator.evaluate(action_spec)

        base_explanation = {
            "what": f"Action request: {action_spec.action_type}",
            "why": "Action evaluated by GuardedExecutor",
            "risk_level": action_spec.risk_level,
            "details": {
                "required_scopes": list(action_spec.required_scopes),
            },
        }

        # Permission denied
        if not decision.allowed:
            return ExecutionPlan(
                action_type=action_spec.action_type,
                target=action_spec.target,
                parameters=action_spec.parameters,
                risk_level=action_spec.risk_level,
                required_scopes=set(action_spec.required_scopes),
                explanation={
                    **base_explanation,
                    "permission": "DENIED",
                    "prompt": decision.prompt_payload,
                },
                dry_run=True,
            )

        # Confirmation required
        if decision.requires_confirmation:
            return ExecutionPlan(
                action_type=action_spec.action_type,
                target=action_spec.target,
                parameters=action_spec.parameters,
                risk_level=action_spec.risk_level,
                required_scopes=set(action_spec.required_scopes),
                explanation={
                    **base_explanation,
                    "permission": "CONFIRMATION_REQUIRED",
                    "prompt": decision.prompt_payload,
                },
                dry_run=True,
            )

        # LOW-RISK LIVE EXECUTION ONLY
        if action_spec.action_type == "OPEN_APP":
            result = AppControl.open_app(
                action_spec.parameters["app_name"]
            )
        elif action_spec.action_type == "SYSTEM_INFO":
            result = SystemInfo.uname()
        else:
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
                **base_explanation,
                "permission": "GRANTED",
                "result": result,
            },
            dry_run=False,
        )
