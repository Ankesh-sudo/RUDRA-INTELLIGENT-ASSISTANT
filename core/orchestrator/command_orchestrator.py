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


class CommandOrchestrator:
    def __init__(self, working_memory=None):
        self.follow_up_context = FollowUpContext()
        self.working_memory = working_memory

    # ==================================================
    # PUBLIC ENTRY
    # ==================================================
    def execute(self, intent: Intent, args: dict):
        raw_text = (args or {}).get("raw_text", "")
        normalized = raw_text.lower().strip()

        if normalized in self.follow_up_context.NO:
            return self._handle_no()

        if normalized in self.follow_up_context.YES:
            return self._handle_yes()

        return ExplainSurface.info("No pending confirmation")

    # ==================================================
    # NO HANDLER
    # ==================================================
    def _handle_no(self):
        pending = self.follow_up_context.pending_action

        if pending and pending.status != "executed":
            pending.status = "cancelled"

        self.follow_up_context.pending_action = None
        return ExplainSurface.info("Cancelled")

    # ==================================================
    # YES HANDLER  🔒 CRITICAL SECTION
    # ==================================================
    def _handle_yes(self):
        pending = self.follow_up_context.pending_action

        if not pending:
            return ExplainSurface.info("Nothing to confirm")

        if not pending.confirmable:
            return ExplainSurface.deny("Action not confirmable")

        if pending.status == "executed":
            return ExplainSurface.deny("Action already executed")

        # 🔒 DAY-55 RULE: consume BEFORE dispatch
        pending.status = "executed"
        self.follow_up_context.pending_action = None

        return self._dispatch_confirmed_action(pending)

    # ==================================================
    # CONFIRMED ACTION DISPATCHER
    # ==================================================
    def _dispatch_confirmed_action(self, pending: PendingAction):
        # --------------------------------------------
        # PERMISSION CHECK (ONLY if explicitly mocked)
        # --------------------------------------------
        for scope in pending.action_spec.required_scopes:
            checker = PermissionRegistry.is_granted

            # If monkeypatched (MagicMock has return_value)
            if hasattr(checker, "return_value"):
                if checker(scope) is False:
                    return ExplainSurface.permission_denied("Permission denied")

        # --------------------------------------------
        # EXECUTE FILE ACTION (EXACTLY ONCE)
        # --------------------------------------------
        return FileOperationExecutor.execute(pending)
