from typing import Dict, Any

from core.nlp.intent import Intent
from core.explain.explain_surface import ExplainSurface
from core.skills.system_actions import open_app as system_open_app


# -------------------------------------------------
# Day 53 — local follow-up slot (SAFE, isolated)
# -------------------------------------------------
_PENDING_APP_NAME = False


def handle(intent: Intent, args: Dict[str, Any]):
    global _PENDING_APP_NAME

    raw_text = (args or {}).get("raw_text", "").strip().lower()

    # -----------------------------------------
    # YES / NO → NOOP (OPEN_APP has no confirm)
    # -----------------------------------------
    if raw_text in {"yes", "no"}:
        return {
            "type": "noop",
            "message": "Nothing to confirm.",
        }

    if intent != Intent.OPEN_APP:
        return ExplainSurface.deny("Unsupported app action")

    # -----------------------------------------
    # FOLLOW-UP SLOT COMPLETION
    # -----------------------------------------
    if _PENDING_APP_NAME:
        _PENDING_APP_NAME = False
        return _execute_open(raw_text)

    app_name = args.get("app_name")

    # -----------------------------------------
    # SLOT MISSING → ASK
    # -----------------------------------------
    if not app_name:
        _PENDING_APP_NAME = True
        return {
            "type": "awaiting_follow_up",
            "message": "Which app should I open?",
            "payload": None,
        }

    return _execute_open(app_name)


def _execute_open(app_name: str):
    result = system_open_app({"app_name": app_name})

    if not isinstance(result, dict):
        return ExplainSurface.deny("Invalid system response")

    if result.get("success"):
        return {
            "type": "action_result",
            "message": result.get("message", "Application opened"),
            "result": result,
        }

    return ExplainSurface.deny(
        result.get("message", "Failed to open application")
    )
