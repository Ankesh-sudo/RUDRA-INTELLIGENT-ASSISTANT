"""
Action Executor
Day 17.6 — Confidence Gating + Follow-up + Slot Recovery (FINAL)
Day 18.1 — Global Interrupt Guard (READ-ONLY)
Day 18.3 — Safe Cancel Hook (FINAL)
Day 18.4 — Policy-Compatible (NO OWNERSHIP)

Day 50 — OS Control Integration (GUARDED)
"""

import logging
from typing import Dict, Any, Optional, List

from core.nlp.intent import Intent
from core.nlp.argument_extractor import ArgumentExtractor
from core.context.follow_up import FollowUpContext
from core.control.global_interrupt import GLOBAL_INTERRUPT

# OS execution layer
from core.os.executor.guarded_executor import GuardedExecutor
from core.os.action_spec import ActionSpec

# App name → executable resolution
from core.system.app_registry import AppRegistry

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Required arguments per intent
# -------------------------------------------------
REQUIRED_ARGS = {
    "open_app": ["app_name"],
    "run_command": ["command"],
    "list_files": ["path"],
    "open_file": ["filename"],
    "system_info": [],
}


class ActionExecutor:
    def __init__(self, config=None):
        self.config = config
        self.argument_extractor = ArgumentExtractor(config)
        self.follow_up_context = FollowUpContext()
        self.guarded_executor = GuardedExecutor()

        self.min_confidence = 0.3
        self.action_history: List[Dict[str, Any]] = []

    # -------------------------------------------------
    # SAFE CANCEL
    # -------------------------------------------------
    def cancel_pending(self):
        self.follow_up_context.clear_context()

    # -------------------------------------------------
    # EXECUTION ENTRY
    # -------------------------------------------------
    def execute(
        self,
        intent: Intent,
        text: str,
        confidence: float,
        replay_args: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        # 🔴 HARD INTERRUPT GUARD
        if GLOBAL_INTERRUPT.is_triggered():
            return {
                "success": False,
                "message": "Action cancelled.",
                "confidence": confidence,
                "executed": False,
            }

        # ❌ UNKNOWN OR LOW CONFIDENCE
        if intent == Intent.UNKNOWN or confidence < self.min_confidence:
            return {
                "success": False,
                "message": "Intent not supported.",
                "confidence": confidence,
                "executed": False,
            }

        # ---------------- ARGUMENT EXTRACTION ----------------
        args = self.argument_extractor.extract_for_intent(text, intent.value) or {}

        # Single-word recovery for OPEN_APP
        if intent == Intent.OPEN_APP and not args.get("app_name"):
            if text.strip() and len(text.split()) == 1:
                args["app_name"] = text.strip()

        if replay_args:
            args.update(replay_args)

        # ---------------- SLOT CHECK ----------------
        for slot in REQUIRED_ARGS.get(intent.value, []):
            if not args.get(slot):
                return {
                    "success": False,
                    "message": f"Please provide {slot}.",
                    "confidence": confidence,
                    "executed": False,
                }

        # ---------------- OS ACTION PATH ----------------
        plan = self._execute_os_action(intent, args)

        if plan is None:
            return {
                "success": False,
                "message": f"Intent not implemented: {intent.value}",
                "confidence": confidence,
                "executed": False,
            }

        permission = plan.explanation.get("permission")

        if permission == "DENIED":
            return {
                "success": False,
                "message": "Permission denied.",
                "confidence": confidence,
                "executed": False,
            }

        if permission == "CONFIRMATION_REQUIRED":
            return {
                "success": False,
                "message": "This action needs your confirmation.",
                "confidence": confidence,
                "executed": False,
            }

        return {
            "success": True,
            "message": "Action executed.",
            "confidence": confidence,
            "executed": True,
            "result": plan.explanation.get("result"),
        }

    # -------------------------------------------------
    # OS ACTION MAPPING — FIXED & COMPLETE
    # -------------------------------------------------
    def _execute_os_action(self, intent: Intent, args: Dict[str, Any]):

        # ---------------- OPEN APPLICATION ----------------
        if intent in {Intent.OPEN_APP, Intent.OPEN_TERMINAL}:
            app_name = args.get("app_name", "terminal")
            resolved_app = AppRegistry.resolve(app_name)

            spec = ActionSpec(
                action_type="OPEN_APP",
                category="APP",
                target=resolved_app,
                parameters={"app_name": resolved_app},
                risk_level="LOW",
                destructive=False,
                supports_undo=False,
                requires_preview=False,
                required_scopes=set(),  # ✅ SAFE
            )
            return self.guarded_executor.execute(spec)

        # ---------------- OPEN BROWSER / YOUTUBE ----------------
        if intent in {Intent.OPEN_BROWSER, Intent.OPEN_YOUTUBE}:
            url = "https://www.youtube.com" if intent == Intent.OPEN_YOUTUBE else None

            spec = ActionSpec(
                action_type="OPEN_BROWSER",
                category="WEB",
                target=url or "browser",
                parameters={"url": url},
                risk_level="LOW",
                destructive=False,
                supports_undo=False,
                requires_preview=False,
                required_scopes=set(),  # ✅ SAFE
            )
            return self.guarded_executor.execute(spec)

        # ---------------- RUN TERMINAL COMMAND ----------------
        if intent == Intent.RUN_COMMAND:
            spec = ActionSpec(
                action_type="RUN_COMMAND",
                category="SYSTEM",
                target="terminal",
                parameters={"command": args["command"]},
                risk_level="HIGH",
                destructive=False,
                supports_undo=False,
                requires_preview=True,
                required_scopes={"TERMINAL_EXEC"},
            )
            return self.guarded_executor.execute(spec)

        # ---------------- SYSTEM INFO ----------------
        if intent == Intent.SYSTEM_INFO:
            spec = ActionSpec(
                action_type="SYSTEM_INFO",
                category="SYSTEM",
                target="system",
                parameters={},
                risk_level="LOW",
                destructive=False,
                supports_undo=False,
                requires_preview=False,
                required_scopes=set(),
            )
            return self.guarded_executor.execute(spec)

        return None
