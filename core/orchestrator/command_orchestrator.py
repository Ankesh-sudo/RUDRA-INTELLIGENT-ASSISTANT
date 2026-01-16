"""
Command Orchestrator
Single authoritative gateway for intent execution.

Day 55 UPDATE:
- Explicit PendingAction confirmation hook
- Single-use consumption
- No re-inference, no re-resolution
- Execution dispatcher stub only (no mutation yet)
"""

from core.skills.skill_registry import SKILL_REGISTRY, Skill
from core.nlp.intent import Intent
from core.skills import system_actions

from core.os.permission.permission_registry import PermissionRegistry
from core.os.permission.consent_prompt import ConsentPrompt

from core.context.pending_action import PendingAction
from core.context.follow_up import FollowUpContext
from core.explain.explain_surface import ExplainSurface


class CommandOrchestrator:
    def __init__(self):
        # 🟦 Follow-up & pending-action manager (Day 53 locked)
        self.follow_up_context = FollowUpContext()

    # -------------------------------------------------
    # PUBLIC ENTRY
    # -------------------------------------------------
    def execute(self, intent: Intent, args: dict):
        """
        args MUST include raw_text for follow-up resolution:
        {
            "raw_text": "...",
            ...
        }
        """

        raw_text = args.get("raw_text", "")
        normalized = raw_text.lower().strip()

        # =================================================
        # 🟦 DAY 55 — CONFIRMATION HOOK (ACTION-BASED)
        # =================================================
        pending_action = self.follow_up_context.pending_action

        if normalized == "yes" and pending_action:
            return self._handle_confirmation(pending_action)

        # =================================================
        # 🟦 DAY 53 — LEGACY FOLLOW-UP RESOLUTION
        # =================================================
        pending = self.follow_up_context.resolve_pending_action(raw_text)
        if pending:
            return self.execute(pending.intent, pending.args)

        # =================================================
        # 🟦 YES / NO WITH NO PENDING ACTION → SAFE NO-OP
        # =================================================
        if normalized in {
            "yes", "yeah", "yep", "ok", "okay", "sure",
            "no", "nope", "cancel"
        }:
            # No pending action → explicit, explainable no-op
            return ExplainSurface.info("Nothing to confirm")

        # -------------------------------------------------
        # Resolve skill ownership
        # -------------------------------------------------
        skill = SKILL_REGISTRY.get(intent)
        if not skill:
            return ExplainSurface.error("Intent not implemented")

        if skill == Skill.SYSTEM:
            return self._execute_system(intent, args)

        return ExplainSurface.error("Skill not supported yet")

    # -------------------------------------------------
    # CONFIRMATION HANDLER (DAY 55 — STRICT)
    # -------------------------------------------------
    def _handle_confirmation(self, pending_action: PendingAction):
        # ❌ Invalid or already-consumed pending action
        if not pending_action.is_confirmable():
            return ExplainSurface.deny("Pending action is not confirmable")

        # 🔒 Freeze point — DO NOT re-run NLP / resolution
        try:
            result = self._dispatch_confirmed_action(pending_action)
            pending_action.mark_executed()
        finally:
            # Consume pending action exactly once
            self.follow_up_context.clear_pending_action()

        return result

    # -------------------------------------------------
    # CONFIRMED ACTION DISPATCHER (STUB — NO MUTATION)
    # -------------------------------------------------
    def _dispatch_confirmed_action(self, pending_action: PendingAction):
        spec = pending_action.action_spec

        # ❌ Only FILE actions allowed here (Day 55 scope)
        if not spec or spec.category != "FILE":
            return ExplainSurface.deny("Unsupported confirmed action type")

        # 🔐 Permission enforcement via required_scopes
        for scope in spec.required_scopes or set():
            if not PermissionRegistry.is_action_allowed(scope):
                return ExplainSurface.permission_denied(scope)

        # ⚠️ EXECUTION STUB ONLY (Task 2 will replace this)
        return ExplainSurface.info(
            "Confirmation accepted. Execution dispatcher reached.",
            payload={
                "category": spec.category,
                "required_scopes": list(spec.required_scopes or []),
                "preview": pending_action.preview_data,
                "next_step": "FileOperationExecutor (Day 55 Task 2)",
            },
        )

    # -------------------------------------------------
    # SYSTEM SKILL (UNCHANGED)
    # -------------------------------------------------
    def _execute_system(self, intent: Intent, args: dict):
        # ---------------- OPEN_APP ----------------
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
    # PERMISSION FLOW (UNCHANGED & SAFE)
    # -------------------------------------------------
    def _execute_with_permission(
        self,
        action_type: str,
        action_callable,
        args: dict,
    ):
        """
        Preserved behavior:
        - If permission granted → execute
        - If permission missing → return consent payload
        """

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
