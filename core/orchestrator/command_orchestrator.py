"""
Command Orchestrator
Single authoritative gateway for intent execution.

DAY 59 — Execution Session Manager (LOCKED):

- No action execution
- No permission checks
- No OS calls
- One command → one ExecutionSession
- Returns explainable session summary only
"""

import uuid

from core.skills.skill_registry import SKILL_REGISTRY, Skill
from core.nlp.intent import Intent

from core.context.pending_action import PendingAction
from core.context.follow_up import FollowUpContext
from core.explain.explain_surface import ExplainSurface

from core.actions.action_planner import ActionPlanner
from core.orchestrator.execution_session import ExecutionSession


class CommandOrchestrator:
    def __init__(self, working_memory=None):
        self.follow_up_context = FollowUpContext()
        self.working_memory = working_memory

    # -------------------------------------------------
    # PUBLIC ENTRY (SESSION-BASED)
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

            # Day 59 rule: confirmation does NOT execute
            self.follow_up_context.pending_action = None
            return ExplainSurface.info("Confirmed (execution deferred)")

        # =================================================
        # 🟦 SLOT / FOLLOW-UP RESOLUTION (NOT yes/no)
        # =================================================
        pending = self.follow_up_context.resolve_pending_action(raw_text)
        if pending:
            # Day 59: still no execution
            self.follow_up_context.pending_action = None
            return ExplainSurface.info("Follow-up resolved (execution deferred)")

        # -------------------------------------------------
        # NORMAL INTENT → SESSION CREATION
        # -------------------------------------------------
        skill = SKILL_REGISTRY.get(intent)
        if not skill:
            return ExplainSurface.error("Intent not implemented")

        # -------------------------------------------------
        # 🧠 PLAN ACTIONS (NO EXECUTION)
        # -------------------------------------------------
        try:
            planned_actions = ActionPlanner.plan(intent=intent, args=args)
        except Exception as exc:
            return ExplainSurface.error(
                f"Planning failed: {exc}"
            )

        # -------------------------------------------------
        # 🧩 CREATE EXECUTION SESSION
        # -------------------------------------------------
        session = ExecutionSession(
            session_id=str(uuid.uuid4()),
            working_memory=self.working_memory,
        )
        session.attach_plan(planned_actions)

        # -------------------------------------------------
        # 📤 RETURN EXPLAINABLE SESSION SUMMARY
        # -------------------------------------------------
        return ExplainSurface.plan(
            message="Execution session created",
            payload=session.summary(),
        )
