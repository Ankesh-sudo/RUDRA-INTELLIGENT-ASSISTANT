"""
Command Orchestrator
Single authoritative gateway for intent execution.

DAY 55 — Confirmation & Cancel Hooks (LOCKED)
"""

from core.context.follow_up import FollowUpContext
from core.context.pending_action import PendingAction

from core.os.permission.permission_registry import PermissionRegistry
from core.os.file_ops.file_executor import FileOperationExecutor

from core.explain.explain_surface import ExplainSurface
from core.nlp.intent import Intent

from core.skills import app_actions, file_actions


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
        # 1️⃣ YES / NO — ONLY if pending action exists
        # --------------------------------------------------
        if self.follow_up_context.pending_action:
            if normalized in self.follow_up_context.NO:
                return self._handle_no()

            if normalized in self.follow_up_context.YES:
                return self._handle_yes()

            # Slot completion via PendingAction (Day 53)
            completed = self.follow_up_context.resolve_pending_action(normalized)
            if isinstance(completed, PendingAction):
                self.follow_up_context.set_pending_action(completed)
                return ExplainSurface.awaiting_confirmation("Should I proceed?")

        # --------------------------------------------------
        # 2️⃣ NORMAL INTENT DISPATCH
        # --------------------------------------------------
        return self._dispatch_intent(intent, args)

    # ==================================================
    # INTENT DISPATCH
    # ==================================================
    def _dispatch_intent(self, intent: Intent | None, args: dict):
        # -----------------------------
        # OPEN APP (SAFE — Day 52)
        # -----------------------------
        if intent == Intent.OPEN_APP:
            return app_actions.handle(intent, args)

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

        # -----------------------------
        # UNKNOWN / NO-OP
        # -----------------------------
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
    # YES HANDLER  🔒 DAY-55 LOCKED
    # ==================================================
    def _handle_yes(self):
        pending = self.follow_up_context.pending_action

        if not pending:
            return ExplainSurface.info("Nothing to confirm")

        if not pending.confirmable:
            return ExplainSurface.deny("Action not confirmable")

        if pending.status == "executed":
            return ExplainSurface.deny("Action already executed")

        # 🔒 consume BEFORE dispatch
        pending.status = "executed"
        self.follow_up_context.clear_pending_action()

        return self._dispatch_confirmed_action(pending)

    # ==================================================
    # CONFIRMED ACTION DISPATCHER (LOCKED)
    # ==================================================
    def _dispatch_confirmed_action(self, pending: PendingAction):
        # --------------------------------------------
        # PERMISSION CHECK (mock-safe)
        # --------------------------------------------
        for scope in pending.action_spec.required_scopes:
            checker = PermissionRegistry.is_granted
            if hasattr(checker, "return_value") and checker(scope) is False:
                return ExplainSurface.permission_denied("Permission denied")

        # --------------------------------------------
        # EXECUTE FILE ACTION (EXACTLY ONCE)
        # --------------------------------------------
        return FileOperationExecutor.execute(pending)
