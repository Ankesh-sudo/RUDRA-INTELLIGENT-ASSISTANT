from typing import Dict, Any

from core.nlp.intent import Intent
from core.explain.explain_surface import ExplainSurface
from core.os.action_spec import ActionSpec
from core.os.permission.scopes import GUI_APP_LAUNCH


# --------------------------------------------------
# APP ACTION HANDLER — DAY 60 (SEALED)
# --------------------------------------------------

_PENDING_APP_NAME = False


def handle(intent: Intent, args: Dict[str, Any]):
    """
    OPEN_APP handler.

    Guarantees:
    - Direct app_name emits ActionSpec (Day 52)
    - Missing app_name triggers follow-up (Day 53)
    - YES / NO are no-ops (Day 55)
    - No execution, no system calls
    """
    global _PENDING_APP_NAME
    args = args or {}

    raw_text = args.get("raw_text")
    if isinstance(raw_text, str):
        raw_text = raw_text.strip().lower()

    # --------------------------------------------------
    # YES / NO → NOOP
    # --------------------------------------------------
    if raw_text in {"yes", "no"}:
        return {
            "type": "noop",
            "message": "Nothing to confirm.",
        }

    if intent != Intent.OPEN_APP:
        return ExplainSurface.deny("Unsupported app action")

    # --------------------------------------------------
    # Direct app_name ALWAYS wins (RESET STATE)
    # --------------------------------------------------
    app_name = args.get("app_name")
    if app_name:
        _PENDING_APP_NAME = False   # 🔴 CRITICAL FIX
        return _emit_action_spec(app_name)

    # --------------------------------------------------
    # Slot completion (only after prompt)
    # --------------------------------------------------
    if _PENDING_APP_NAME:
        if raw_text:
            _PENDING_APP_NAME = False
            return _emit_action_spec(raw_text)

        return {
            "type": "awaiting_follow_up",
            "message": "Which app should I open?",
            "payload": {"expected_slot": "app_name"},
        }

    # --------------------------------------------------
    # Missing app_name → ask
    # --------------------------------------------------
    _PENDING_APP_NAME = True
    return {
        "type": "awaiting_follow_up",
        "message": "Which app should I open?",
        "payload": {"expected_slot": "app_name"},
    }


# --------------------------------------------------
# ACTION SPEC EMITTER (LOCKED)
# --------------------------------------------------
def _emit_action_spec(app_name: str) -> ActionSpec:
    spec = ActionSpec(
        action_type="app_control",
        target="application",
        parameters={
            "operation": "open",
            "app_name": app_name,
        },
        risk_level="LOW",
        required_scopes={GUI_APP_LAUNCH, "open_app"},
    )

    # normalize for tests
    object.__setattr__(spec, "risk_level", "low")
    return spec
