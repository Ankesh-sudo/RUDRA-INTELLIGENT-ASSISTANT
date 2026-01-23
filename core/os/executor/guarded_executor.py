from dataclasses import dataclass
from typing import Any, Dict, Set

from core.os.executor.executor_contract import ExecutorContract
from core.os.executor.dry_run_backend import DryRunBackend
from core.os.executor.os_control_stub import OSControlStubExecutor
from core.os.permission.consent_store import ConsentStore
from core.os.permission.permission_evaluator import PermissionEvaluator

from core.os.control_capabilities import OSControlCapability
from core.os.linux.linux_backend import LinuxBackend
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

    Day 61:
    - OS_CONTROL stubbed

    Day 64:
    - SAFE OS_CONTROL enabled for:
        • OPEN_BROWSER
        • OPEN_URL
        • OPEN_APP
    """

    def __init__(self):
        self._backend = DryRunBackend()
        self._consent_store = ConsentStore()
        self._permission_evaluator = PermissionEvaluator(self._consent_store)

    def execute(self, action_spec):
        if action_spec is None:
            raise ValueError("ActionSpec is required")

        # --------------------------------------------------
        # DAY 64 — SAFE OS CONTROL (PARTIAL ENABLE)
        # --------------------------------------------------
        if action_spec.category == "OS_CONTROL":
            capability = action_spec.capability

            # ---------------- SAFE ENABLED ----------------
            if capability in {
                OSControlCapability.OPEN_BROWSER,
                OSControlCapability.OPEN_URL,
                OSControlCapability.OPEN_APP,
            }:
                # Permission still enforced
                decision = self._permission_evaluator.evaluate(action_spec)

                if not decision.allowed:
                    return ExecutionPlan(
                        action_type=action_spec.action_type,
                        target=action_spec.target,
                        parameters=action_spec.parameters,
                        risk_level=action_spec.risk_level,
                        required_scopes=set(action_spec.required_scopes),
                        explanation={
                            "permission": "DENIED",
                            "prompt": decision.prompt_payload,
                        },
                        dry_run=True,
                    )

                if decision.requires_confirmation:
                    return ExecutionPlan(
                        action_type=action_spec.action_type,
                        target=action_spec.target,
                        parameters=action_spec.parameters,
                        risk_level=action_spec.risk_level,
                        required_scopes=set(action_spec.required_scopes),
                        explanation={
                            "permission": "CONFIRMATION_REQUIRED",
                            "prompt": decision.prompt_payload,
                        },
                        dry_run=True,
                    )

                # ---------------- REAL EXECUTION ----------------
                if capability == OSControlCapability.OPEN_BROWSER:
                    LinuxBackend.open_browser()

                elif capability == OSControlCapability.OPEN_URL:
                    LinuxBackend.open_url(
                        action_spec.parameters.get("url")
                    )

                elif capability == OSControlCapability.OPEN_APP:
                    LinuxBackend.open_application(
                        action_spec.parameters.get("app")
                    )

                return ExecutionPlan(
                    action_type=action_spec.action_type,
                    target=action_spec.target,
                    parameters=action_spec.parameters,
                    risk_level=action_spec.risk_level,
                    required_scopes=set(action_spec.required_scopes),
                    explanation={
                        "permission": "GRANTED",
                        "status": "executed",
                        "capability": capability,
                    },
                    dry_run=False,
                )

            # ---------------- STILL STUBBED ----------------
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
                        f"OS control capability '{capability}' "
                        "is declared but not executable yet."
                    ),
                    "permission": "DENIED",
                    "details": {
                        "capability": capability,
                        "parameters": action_spec.parameters or {},
                    },
                },
                dry_run=True,
            )

        # --------------------------------------------------
        # DAY 48–50 FLOW (LOCKED, NON-OS)
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

        # LOW-RISK NON-OS EXECUTION (UNCHANGED)
        if action_spec.action_type == "OPEN_APP":
            app_name = action_spec.parameters.get("app_name")
            if not app_name:
                result = {
                    "ok": True,
                    "error": "Application name missing",
                },
            else:
                LinuxBackend.open_application(app_name)
                result = {"ok": True}

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
                "permission": "GRANTED",
                "status": "executed",
                "result": result,
            },
            dry_run=False,
        )
