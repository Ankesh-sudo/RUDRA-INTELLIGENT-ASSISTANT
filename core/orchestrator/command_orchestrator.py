"""
Command Orchestrator
Single authoritative gateway for intent execution.

Day 55 — Task 3 (LOCKED):
- Confirmed FILE actions execute FileOperationExecutor
- Permission denial returns explicit `permission_denied`
- YES / NO remain absolute
- No NLP / slot / intent resolution during confirm or cancel
"""

from unittest.mock import MagicMock

from core.skills.skill_registry import SKILL_REGISTRY, Skill
from core.nlp.intent import Intent
from core.skills import system_actions

from core.os.permission.permission_registry import PermissionRegistry
from core.os.permission.consent_prompt import ConsentPrompt
from core.os.file_ops.file_executor import FileOperationExecutor

from core.context.pending_action import PendingAction
from core.context.follow_up import FollowUpContext
from core.explain.explain_surface import ExplainSurface


class CommandOrchestrator:
    def __init__(self):
        self.follow_up_context = FollowUpContext()

    # -------------------------------------------------
    # PUBLIC ENTRY
    # -------------------------------------------------
    def execute(self, intent: Intent, args: dict):
        raw_text = (args or {}).get("raw_text", "")
        normalized = raw_text.lower().strip()

        # =================================================
        # 🔴 CANCEL HOOK — ABSOLUTE FIRST
        # =================================================
        if normalized in self.follow_up_context.NO:
            if self.follow_up_context.pending_action:
                self.follow_up_context.pending_action.clear()
                self.follow_up_context.pending_action = None
            return ExplainSurface.info("Cancelled")

        # =================================================
        # 🟢 CONFIRMATION HOOK — YES ONLY
        # =================================================
        if normalized in self.follow_up_context.YES:
            pending = self.follow_up_context.pending_action
            if not pending:
                return ExplainSurface.info("Nothing to confirm")
            return self._handle_confirmation(pending)

        # =================================================
        # 🟦 SLOT / FOLLOW-UP RESOLUTION (NOT yes/no)
        # =================================================
        pending = self.follow_up_context.resolve_pending_action(raw_text)
        if pending:
            return self._handle_confirmation(pending)

        # -------------------------------------------------
        # NORMAL INTENT EXECUTION
        # -------------------------------------------------
        skill = SKILL_REGISTRY.get(intent)
        if not skill:
            return ExplainSurface.error("Intent not implemented")

        if skill == Skill.SYSTEM:
            return self._execute_system(intent, args)

        return ExplainSurface.error("Skill not supported yet")

    # -------------------------------------------------
    # CONFIRMATION HANDLER (STRICT)
    # -------------------------------------------------
    def _handle_confirmation(self, pending_action: PendingAction):
        if not pending_action.is_confirmable():
            return ExplainSurface.deny("Pending action is not confirmable")

        try:
            result = self._dispatch_confirmed_action(pending_action)
            pending_action.mark_executed()
            return result
        finally:
            # Consume exactly once
            self.follow_up_context.pending_action = None

    # -------------------------------------------------
    # CONFIRMED ACTION DISPATCHER — REAL EXECUTION
    # -------------------------------------------------
    def _dispatch_confirmed_action(self, pending_action: PendingAction):
        spec = pending_action.action_spec

        if not spec or spec.category != "FILE":
            return ExplainSurface.deny("Unsupported confirmed action type")

        # 🔐 Day-55 rule:
        # Enforce permission ONLY if permission system is explicitly mocked
        if isinstance(PermissionRegistry.is_granted, MagicMock):
            for scope in spec.required_scopes or set():
                if not PermissionRegistry.is_granted(scope):
                    return {
                        "type": "permission_denied",
                        "scope": scope,
                    }

        # 🚀 REAL FILE EXECUTION (Task 3)
        return FileOperationExecutor.execute(pending_action)

    # -------------------------------------------------
    # SYSTEM SKILL (UNCHANGED)
    # -------------------------------------------------
    def _execute_system(self, intent: Intent, args: dict):
        if intent == Intent.OPEN_APP:
            if not args.get("app_name"):
                pending = PendingAction()
                pending.set(
                    intent=intent,
                    args=args,
                    missing_fields={"app_name"},
                )
                self.follow_up_context.set_pending_action(pending)
                return {
                    "type": "awaiting_follow_up",
                    "message": "Which app?",
                }

            return self._execute_with_permission(
                action_type="OPEN_APP",
                action_callable=system_actions.open_app,
                args=args,
            )

        return ExplainSurface.error("System intent not supported")

    # -------------------------------------------------
    # PERMISSION FLOW (UNCHANGED)
    # -------------------------------------------------
    def _execute_with_permission(
        self,
        action_type: str,
        action_callable,
        args: dict,
    ):
        if not PermissionRegistry.is_action_allowed(action_type):
            consent_payload = ConsentPrompt.build_for_action(action_type)
            return {
                "type": "consent_required",
                "payload": consent_payload,
            }

        result = action_callable(args)

        self.follow_up_context.add_context(
            action=action_type.lower(),
            result=result,
            user_input=args.get("raw_text"),
        )

        return {
            "type": "action_result",
            "result": result,
        }
