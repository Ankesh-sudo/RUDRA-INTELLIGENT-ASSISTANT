"""
Action Executor with Confidence Gating
"""

import logging
from typing import Dict, Any, Tuple
from core.nlp.intent import Intent
from core.nlp.argument_extractor import ArgumentExtractor
from core.skills.system_actions import SystemActions

logger = logging.getLogger(__name__)


class ActionExecutor:
    def __init__(self, config=None):
        self.config = config
        self.argument_extractor = ArgumentExtractor(config)
        self.system_actions = SystemActions(config)

        self.min_confidence = 0.3
        self.high_confidence = 0.7

        self.action_history = []

    def execute(self, intent: Intent, text: str, confidence: float) -> Dict[str, Any]:
        logger.info(f"Intent={intent.value} confidence={confidence:.2f}")

        allowed, reason = self._check_confidence(intent, confidence, text)
        if not allowed:
            return {
                "success": False,
                "message": self._rejection_message(reason, confidence),
                "confidence": confidence,
                "executed": False,
                "reason": reason
            }

        args = self.argument_extractor.extract_for_intent(text, intent.value)
        valid, msg = self.argument_extractor.validate_arguments(args, intent.value)
        if not valid:
            return {
                "success": False,
                "message": msg,
                "confidence": confidence,
                "executed": False
            }

        result = self._execute_intent(intent, args)
        self._log(intent, text, confidence, result)

        return {
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "confidence": confidence,
            "executed": True,
            "result": result
        }

    def _execute_intent(self, intent: Intent, args: Dict[str, Any]) -> Dict[str, Any]:
        if intent == Intent.OPEN_BROWSER:
            return self.system_actions.open_browser(
                url=args.get("url"), target=args.get("target")
            )

        if intent == Intent.OPEN_TERMINAL:
            return self.system_actions.open_terminal(
                command=args.get("command"), target=args.get("target")
            )

        if intent == Intent.OPEN_FILE_MANAGER:
            return self.system_actions.open_file_manager(
                path=args.get("path"), target=args.get("target")
            )

        if intent == Intent.SEARCH_WEB:
            return self.system_actions.search_web(
                query=args.get("query"), target=args.get("target")
            )

        if intent == Intent.OPEN_FILE:
            return self.system_actions.open_file(
                filename=args.get("filename"),
                full_path=args.get("full_path"),
                target=args.get("target")
            )

        if intent == Intent.LIST_FILES:
            return self.system_actions.list_files(
                path=args.get("path"), target=args.get("target")
            )

        return {
            "success": False,
            "message": f"Intent not implemented: {intent.value}"
        }

    def _check_confidence(self, intent: Intent, confidence: float, text: str):
        """
        Decide whether an action should be executed based on confidence.
        Aligned with intent_scorer.py
        """

        # Basic intents that always execute
        basic_intents = {
            Intent.GREETING,
            Intent.HELP,
            Intent.EXIT,
        }

        if intent in basic_intents:
            return True, "basic intent"

        # Low confidence block
        if confidence < self.min_confidence:
            return False, "low confidence"

        # Ambiguous references
        ambiguous = ["it", "that", "there", "the thing"]
        if any(word in text.lower() for word in ambiguous) and confidence < 0.6:
            return False, "ambiguous command"

        # Dangerous actions (terminal)
        if intent == Intent.OPEN_TERMINAL and confidence < self.high_confidence:
            return False, "dangerous action"

        return True, "ok"


    def _rejection_message(self, reason: str, confidence: float) -> str:
        if reason == "low confidence":
            return f"I'm not confident enough ({confidence:.0%}). Please rephrase."
        if reason == "ambiguous command":
            return "I'm not sure what you mean. Please be more specific."
        if reason == "dangerous action":
            return "I need to be more certain before doing that."
        return "I can't perform that action."

    def _log(self, intent: Intent, text: str, confidence: float, result: Dict[str, Any]):
        self.action_history.append({
            "intent": intent.value,
            "text": text,
            "confidence": confidence,
            "success": result.get("success", False)
        })
        if len(self.action_history) > 20:
            self.action_history.pop(0)
