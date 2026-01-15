"""
Action Executor
Day 17.6 — Confidence Gating + Follow-up + Slot Recovery (FINAL)
Day 18.1 — Global Interrupt Guard (READ-ONLY)
Day 18.3 — Safe Cancel Hook (FINAL)
Day 18.4 — Policy-Compatible (NO OWNERSHIP)

Day 50 — OS Control Integration (GUARDED)
- Translates intent → ActionSpec
- Delegates authority to GuardedExecutor
- No direct OS calls
"""

import logging
from typing import Dict, Any, Optional, List

from core.nlp.intent import Intent
from core.nlp.argument_extractor import ArgumentExtractor
from core.context.follow_up import FollowUpContext
from core.control.global_interrupt import GLOBAL_INTERRUPT  # READ-ONLY

# 🟦 Day 50 — OS Control
from core.os.executor.guarded_executor import GuardedExecutor
from core.os.action_spec import ActionSpec
from core.os.permission.scopes import APP_CONTROL, SYSTEM_INFO

logger = logging.getLogger(__name__)

# Never auto-repeat dangerous intents
DANGEROUS_INTENTS = {Intent.OPEN_TERMINAL}

# -------------------------------------------------
# Day 50 — Required arguments (cleaned)
# -------------------------------------------------
REQUIRED_ARGS = {
    "open_app": ["app_name"],
    "open_terminal": ["command"],
    "list_files": ["path"],
    "open_file": ["filename"],
    "system_info": [],
}


class ActionExecutor:
    def __init__(self, config=None):
        self.config = config
        self.argument_extractor = ArgumentExtractor(config)
        self.follow_up_context = FollowUpContext()

        # 🟦 Day 50 — Guarded OS executor
        self.guarded_executor = GuardedExecutor()

        self.min_confidence = 0.3
        self.high_confidence = 0.7
        self.min_reference_confidence = 0.5

        self.action_history: List[Dict[str, Any]] = []

    # =====================================================
    # DAY 18.3 — SAFE CANCEL HOOK
    # =====================================================
    def cancel_pending(self):
        self.follow_up_context.clear_context()

    # =====================================================
    # EXECUTION ENTRY
    # =====================================================
    def execute(
        self,
        intent: Intent,
        text: str,
        confidence: float,
        replay_args: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        # 🔴 HARD GUARD — never clear interrupt here
        if GLOBAL_INTERRUPT.is_triggered():
            logger.warning("Execution skipped due to global interrupt")
            return {
                "success": False,
                "message": "Action cancelled.",
                "confidence": confidence,
                "executed": False,
            }

        logger.info("Intent=%s confidence=%.2f", intent.value, confidence)

        # ---------------- UNKNOWN ----------------
        if intent == Intent.UNKNOWN:
            self.follow_up_context.clear_context()
            return {
                "success": False,
                "message": "Intent not supported",
                "confidence": confidence,
                "executed": False,
            }

        # ---------------- CONFIDENCE GATE ----------------
        if confidence < self.min_confidence:
            return {
                "success": False,
                "message": "I can’t perform that action.",
                "confidence": confidence,
                "executed": False,
            }

        # ---------------- ARGUMENT EXTRACTION ----------------
        args = self.argument_extractor.extract_for_intent(text, intent.value) or {}

        # 🟦 Day 50 — single-word follow-up recovery for OPEN_APP
        if intent == Intent.OPEN_APP and not args.get("app_name"):
            if text.strip() and len(text.split()) == 1:
                args["app_name"] = text.strip()

        if replay_args:
            args = {**args, **replay_args}

        # ---------------- SLOT CHECK ----------------
        for slot in REQUIRED_ARGS.get(intent.value, []):
            if not args.get(slot):
                self.follow_up_context.clear_context()
                return {
                    "success": False,
                    "message": f"Please provide {slot}.",
                    "confidence": confidence,
                    "executed": False,
                }

        # =====================================================
        # 🟦 DAY 50 — OS CONTROL PATH
        # =====================================================
        plan = self._execute_os_action(intent, args)

        if plan is not None:
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

        # ---------------- FALLBACK ----------------
        return {
            "success": False,
            "message": f"Intent not implemented: {intent.value}",
            "confidence": confidence,
            "executed": False,
        }

    # =====================================================
    # 🟦 DAY 50 — OS ACTION MAPPING
    # =====================================================
    def _execute_os_action(self, intent: Intent, args: Dict[str, Any]):
        """
        Maps supported intents to ActionSpec and delegates to GuardedExecutor.
        """

        if intent == Intent.OPEN_APP:
            spec = ActionSpec(
                action_type="OPEN_APP",
                target=args["app_name"],
                parameters={"app_name": args["app_name"]},
                risk_level="LOW",
                required_scopes={APP_CONTROL},
            )
            return self.guarded_executor.execute(spec)

        if intent.value == "system_info":
            spec = ActionSpec(
                action_type="SYSTEM_INFO",
                target="system",
                parameters={},
                risk_level="LOW",
                required_scopes={SYSTEM_INFO},
            )
            return self.guarded_executor.execute(spec)

        return None

    # =====================================================
    # HELPERS
    # =====================================================
    def _log(self, intent: Intent, text: str, confidence: float):
        self.action_history.append(
            {"intent": intent.value, "text": text, "confidence": confidence}
        )
        self.action_history = self.action_history[-20:]
