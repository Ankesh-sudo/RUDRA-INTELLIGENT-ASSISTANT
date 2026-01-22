"""
Command Orchestrator
Single authoritative gateway for intent execution.

DAY 55 — Confirmation & Cancel Hooks (LOCKED)
"""

from core.context.follow_up import FollowUpContext
from core.context.pending_action import PendingAction

from core.os.file_ops.file_executor import FileOperationExecutor
from core.skills.system_actions import open_app as system_open_app

from core.explain.explain_surface import ExplainSurface
from core.nlp.intent import Intent

from core.skills import app_actions, file_actions
from core.os.action_spec import ActionSpec

from core.os.permission.permission_registry import PermissionRegistry


class CommandOrchestrator:
    def __init__(self, working_memory=None):
        self.follow_up_context = FollowUpContext()
        self.working_memory = working_memory

    # ==================================================
    # PUBLIC ENTRY
    # ==================================================
    def execute(self, intent: Intent | None, args: dict | None = None):
        args = args or {}
        raw_text = args.get("raw_text", "")
        normalized = raw_text.lower().strip()

        # --------------------------------------------------
        # YES / NO — ONLY if pending action exists
        # --------------------------------------------------
        if self.follow_up_context.pending_action:
            if normalized in self.follow_up_context.NO:
                return self._handle_no()

            if normalized in self.follow_up_context.YES:
                return self._handle_yes()

            completed = self.follow_up_context.resolve_pending_action(normalized)
            if isinstance(completed, PendingAction):
                self.follow_up_context.set_pending_action(completed)
                return ExplainSurface.awaiting_confirmation("Should I proceed?")

        return self._dispatch_intent(intent, args)

    # ==================================================
    # INTENT DISPATCH
    # ==================================================
    def _dispatch_intent(self, intent: Intent | None, args: dict):
        # -----------------------------
        # OPEN APP — SAFE (Day 52)
        # -----------------------------
        if intent == Intent.OPEN_APP:
            result = app_actions.handle(intent, args)

            if isinstance(result, dict):
                return result

            if isinstance(result, ActionSpec):
                sys_result = system_open_app(result.parameters)

                if sys_result.get("success"):
                    return {
                        "type": "action_result",
                        "message": sys_result.get(
                            "message", "Application opened"
                        ),
                        "result": sys_result,
                    }

                return ExplainSurface.deny(
                    sys_result.get("message", "Failed to open application")
                )

            return ExplainSurface.deny("Invalid app action")

        # -----------------------------
        # DELETE FILE (PREVIEW — Day 54)
        # -----------------------------
        if intent == Intent.DELETE_FILE:
            result = file_actions.handle(intent, args.get("raw_text", ""))

            if not result:
                return ExplainSurface.deny("Invalid file action")

            pending, explain = result
            self.follow_up_context.set_pending_action(pending)
            return explain

        return ExplainSurface.info("No action performed")

    # ==================================================
    # NO HANDLER (LOCKED)
    # ==================================================
    def _handle_no(self):
        pending = self.follow_up_context.pending_action

        if pending and pending.status != "executed":
            pending.status = "cancelled"

        self.follow_up_context.clear_pending_action()
        return ExplainSurface.info("Cancelled")

    # ==================================================
    # YES HANDLER (LOCKED)
    # ==================================================
    def _handle_yes(self):
        pending = self.follow_up_context.pending_action

        if not pending:
            return ExplainSurface.info("Nothing to confirm")

        if not pending.confirmable:
            return ExplainSurface.deny("Action not confirmable")

        if pending.status == "executed":
            return ExplainSurface.deny("Action already executed")

        pending.status = "executed"
        self.follow_up_context.clear_pending_action()

        return self._dispatch_confirmed_action(pending)

    # ==================================================
    # CONFIRMED ACTION DISPATCHER (LOCKED)
    # ==================================================
    def _dispatch_confirmed_action(self, pending: PendingAction):
            for scope in pending.action_spec.required_scopes:
                checker = PermissionRegistry.is_granted
                if hasattr(checker, "return_value") and checker(scope) is False:
                    return ExplainSurface.permission_denied("Permission denied")

            return FileOperationExecutor.execute(pending)
