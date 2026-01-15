"""
Command Orchestrator
Single authoritative gateway for intent execution.

Day 53 FINAL:
- PendingAction slot completion
- Follow-up resolution BEFORE execution
- Safe handling of yes/no with no pending action
- No permission bypass
- No replay regression
"""

from core.skills.skill_registry import SKILL_REGISTRY, Skill
from core.nlp.intent import Intent
from core.skills import system_actions

from core.os.permission.permission_registry import PermissionRegistry
from core.os.permission.consent_prompt import ConsentPrompt

from core.context.pending_action import PendingAction
from core.context.follow_up import FollowUpContext


class CommandOrchestrator:
    def __init__(self):
        # 🟦 Day 53 — follow-up context manager
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
        # 🟦 Day 53 — resolve pending action FIRST
        # =================================================
        pending = self.follow_up_context.resolve_pending_action(raw_text)

        # Case 1: Pending action completed → execute
        if pending:
            return self.execute(pending.intent, pending.args)

        # Case 2: yes/no with NO pending action → ignore safely
        if normalized in {
            "yes", "yeah", "yep", "ok", "okay", "sure",
            "no", "nope", "cancel"
        }:
            return {
                "type": "noop",
                "message": "Nothing to confirm.",
            }

        # -------------------------------------------------
        # Resolve skill ownership
        # -------------------------------------------------
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
        # ---------------- OPEN_APP ----------------
        if intent == Intent.OPEN_APP:
            # 🟦 Day 53 — detect missing slot
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

        return {
            "type": "error",
            "message": "System intent not supported",
        }

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
        Day 50 behavior preserved:

        - If permission granted → execute
        - If permission missing → return consent payload
        """

        # 1. Check permission registry
        if not PermissionRegistry.is_action_allowed(action_type):
            consent_payload = ConsentPrompt.build_for_action(action_type)

            return {
                "type": "consent_required",
                "payload": consent_payload,
            }

        # 2. Execute action
        result = action_callable(args)

        # 3. Store context for replay-safe follow-ups
        self.follow_up_context.add_context(
            action=action_type.lower(),
            result=result,
            user_input=args.get("raw_text"),
        )

        return {
            "type": "action_result",
            "result": result,
        }
