"""
Action Executor with Confidence Gating
Day 15.4 — Reference Confidence + Intent-Class Isolation (TEST-CORRECT)
"""

import logging
from typing import Dict, Any, Optional

from core.nlp.intent import Intent
from core.nlp.argument_extractor import ArgumentExtractor
from core.skills.system_actions import SystemActions
from core.context.follow_up import FollowUpContext

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Day 15 — Intent safety classification
# -------------------------------------------------
DANGEROUS_INTENTS = {
    Intent.OPEN_TERMINAL,
}

INTENT_CLASS = {
    Intent.OPEN_BROWSER: "system",
    Intent.SEARCH_WEB: "system",
    Intent.OPEN_FILE_MANAGER: "filesystem",
    Intent.LIST_FILES: "filesystem",
    Intent.OPEN_FILE: "filesystem",
    Intent.OPEN_TERMINAL: "dangerous",
}


class ActionExecutor:
    def __init__(self, config=None):
        self.config = config
        self.argument_extractor = ArgumentExtractor(config)
        self.system_actions = SystemActions(config)

        # Intent-isolated follow-up memory
        self.follow_up_context = FollowUpContext()

        self.min_confidence = 0.3
        self.high_confidence = 0.7
        self.min_reference_confidence = 0.5

        self.action_history = []

    # =====================================================
    # PUBLIC ENTRY
    # =====================================================
    def execute(
        self,
        intent: Intent,
        text: str,
        confidence: float,
        replay_args: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        logger.info("Intent=%s confidence=%.2f", intent.value, confidence)

        # -------------------------------------------------
        # EXPLICIT REPLAY (tests only)
        # -------------------------------------------------
        if replay_args is not None:
            args = replay_args

        else:
            # -------------------------------------------------
            # FOLLOW-UP PATH
            # -------------------------------------------------
            followup = self._try_follow_up(text, confidence)
            if followup is not None:
                return followup

            # -------------------------------------------------
            # CONFIDENCE GATING
            # -------------------------------------------------
            allowed, reason = self._check_confidence(intent, confidence)
            if not allowed:
                return {
                    "success": False,
                    "message": self._rejection_message(reason, confidence),
                    "confidence": confidence,
                    "executed": False,
                    "reason": reason,
                }

            # -------------------------------------------------
            # ARGUMENT EXTRACTION
            # -------------------------------------------------
            args = self.argument_extractor.extract_for_intent(text, intent.value)
            valid, msg = self.argument_extractor.validate_arguments(args, intent.value)

            if not valid:
                return {
                    "success": False,
                    "message": msg,
                    "confidence": confidence,
                    "executed": False,
                }

        # -------------------------------------------------
        # EXECUTE INTENT
        # -------------------------------------------------
        result = self._execute_intent(intent, args)

        # -------------------------------------------------
        # STORE CONTEXT (SAFE)
        # -------------------------------------------------
        if result.get("success", False):
            self.follow_up_context.add_context(
                action=intent.value,
                result={
                    "success": True,
                    "entities": args,
                    "intent_class": INTENT_CLASS.get(intent),
                    "danger": intent in DANGEROUS_INTENTS,
                },
                user_input=text,
            )

        self._log(intent, text, confidence, result)

        return {
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "confidence": confidence,
            "executed": True,
            "args": args,
            "result": result,
        }

    # =====================================================
    # FOLLOW-UP HANDLING (DAY 15.4 — STRICT)
    # =====================================================
    def _try_follow_up(self, text: str, confidence: float) -> Optional[Dict[str, Any]]:
        text_lower = text.lower()

        reference_words = ("it", "that", "there", "again", "same", "them")
        if not any(w in text_lower for w in reference_words):
            return None

        # Reference confidence gate
        if confidence < self.min_reference_confidence:
            return {
                "success": False,
                "message": "I’m not sure what you want to repeat. Please be specific.",
                "confidence": confidence,
                "executed": False,
            }

        context, reason = self.follow_up_context.resolve_reference(text)

        # 🔒 HARD BLOCK — REQUIRED BY TESTS
        if reason == "cross_intent_blocked":
            logger.warning("[DAY 15.4 BLOCK] Cross-intent follow-up blocked")
            return {
                "success": False,
                "message": "I can’t apply that action to the previous context.",
                "confidence": confidence,
                "executed": False,
                "reason": "cross_intent_blocked",
            }

        if not context:
            return None

        # Dangerous intent isolation
        if context.get("intent_class") == "dangerous":
            return {
                "success": False,
                "message": "I won’t repeat that action for safety.",
                "confidence": confidence,
                "executed": False,
            }

        action = context["action"]

        # ✅ ENTITIES ARE ALREADY SANITIZED BY FollowUpContext
        args = context.get("entities", {})

        result = self._execute_action_by_name(action, args)

        return {
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "confidence": min(1.0, confidence * 1.1),
            "executed": True,
            "args": args,
            "result": result,
            "is_followup": True,
        }

    # =====================================================
    # EXECUTION ROUTER
    # =====================================================
    def _execute_intent(self, intent: Intent, args: Dict[str, Any]) -> Dict[str, Any]:
        return self._execute_action_by_name(intent.value, args)

    def _execute_action_by_name(self, action: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if action == "open_browser":
            return self.system_actions.open_browser(args.get("url"), args.get("target"))
        if action == "search_web":
            return self.system_actions.search_web(args.get("query"), args.get("target"))
        if action == "open_file_manager":
            return self.system_actions.open_file_manager(args.get("path"), args.get("target"))
        if action == "list_files":
            return self.system_actions.list_files(args.get("path"), args.get("target"))
        if action == "open_file":
            return self.system_actions.open_file(
                args.get("filename"), args.get("full_path"), args.get("target")
            )
        if action == "open_terminal":
            return self.system_actions.open_terminal(args.get("command"), args.get("target"))

        return {"success": False, "message": f"Intent not implemented: {action}"}

    # =====================================================
    # SAFETY + LOGGING
    # =====================================================
    def _check_confidence(self, intent: Intent, confidence: float):
        if confidence < self.min_confidence:
            return False, "low confidence"
        if intent in DANGEROUS_INTENTS and confidence < self.high_confidence:
            return False, "dangerous action"
        return True, "ok"

    def _rejection_message(self, reason: str, confidence: float) -> str:
        if reason == "low confidence":
            return f"I'm not confident enough ({confidence:.0%}). Please rephrase."
        if reason == "dangerous action":
            return "I need to be more certain before doing that."
        return "I can’t perform that action."

    def _log(self, intent: Intent, text: str, confidence: float, result: Dict[str, Any]):
        self.action_history.append(
            {
                "intent": intent.value,
                "text": text,
                "confidence": confidence,
                "success": result.get("success", False),
            }
        )
        if len(self.action_history) > 20:
            self.action_history.pop(0)
