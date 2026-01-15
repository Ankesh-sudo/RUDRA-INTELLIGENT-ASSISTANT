"""
Command Orchestrator
Single authoritative gateway for intent execution.

Day 50 FINAL (Corrected):
- OPEN_APP only
- Uses PermissionRegistry (scope-based)
- Does NOT ask user
- Returns consent payload when permission is missing
"""

from core.skills.skill_registry import SKILL_REGISTRY, Skill
from core.nlp.intent import Intent
from core.skills import system_actions

from core.os.permission.permission_registry import PermissionRegistry
from core.os.permission.consent_prompt import ConsentPrompt


class CommandOrchestrator:
    def __init__(self):
        pass

    # -------------------------------------------------
    # PUBLIC ENTRY
    # -------------------------------------------------
    def execute(self, intent: Intent, args: dict):
        # 1. Resolve skill ownership
        skill = SKILL_REGISTRY.get(intent)
        if not skill:
            return {
                "type": "error",
                "message": "Intent not implemented",
            }

        if skill == Skill.SYSTEM:
            return self._execute_system(intent, args)

        return {
            "type": "error",
            "message": "Skill not supported yet",
        }

    # -------------------------------------------------
    # SYSTEM SKILL
    # -------------------------------------------------
    def _execute_system(self, intent: Intent, args: dict):
        if intent == Intent.OPEN_APP:
            return self._execute_with_permission(
                action_type="OPEN_APP",
                action_callable=system_actions.open_app,
                args=args,
            )

        return {
            "type": "error",
            "message": "System intent not supported",
        }

    # -------------------------------------------------
    # PERMISSION FLOW (FINAL & CORRECT)
    # -------------------------------------------------
    def _execute_with_permission(
        self,
        action_type: str,
        action_callable,
        args: dict,
    ):
        """
        Correct Day 50 behavior:

        - If permission granted → execute
        - If permission missing → return consent payload
        """

        # 1. Check permission registry
        if not PermissionRegistry.is_action_allowed(action_type):
            # 2. Build consent payload (NO interaction here)
            consent_payload = ConsentPrompt.build_for_action(action_type)

            return {
                "type": "consent_required",
                "payload": consent_payload,
            }

        # 3. Execute action
        result = action_callable(args)

        return {
            "type": "action_result",
            "result": result,
        }
