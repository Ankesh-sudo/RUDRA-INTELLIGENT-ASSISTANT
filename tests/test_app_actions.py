import pytest

from core.skills.app_actions import handle
from core.nlp.intent import Intent
from core.os.action_spec import ActionSpec


def test_open_app_emits_action_spec():
    result = handle(
        Intent.OPEN_APP,
        {
            "raw_text": "open chrome",
            "app_name": "chrome",
        },
    )

    assert isinstance(result, ActionSpec)
    assert result.action_type == "app_control"
    assert result.target == "application"
    assert result.parameters["operation"] == "open"
    assert result.parameters["app_name"] == "chrome"
    assert "open_app" in result.required_scopes
    assert result.risk_level == "low"


def test_missing_app_name_triggers_follow_up():
    result = handle(Intent.OPEN_APP, {"raw_text": "open app"})

    assert result["type"] == "awaiting_follow_up"
    assert "Which app" in result["message"]
    assert result["payload"]["expected_slot"] == "app_name"


def test_follow_up_cancel_returns_noop():
    result = handle(
        Intent.OPEN_APP,
        {
            "raw_text": "no",
        },
    )

    assert result["type"] == "noop"


def test_non_open_app_intent_is_denied():
    result = handle(Intent.LIST_FILES, {})

    assert result["type"] == "deny"
