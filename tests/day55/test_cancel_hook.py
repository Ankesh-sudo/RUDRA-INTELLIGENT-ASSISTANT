# tests/day55/test_cancel_hook.py

from unittest.mock import MagicMock

from core.orchestrator.command_orchestrator import CommandOrchestrator
from core.context.pending_action import PendingAction
from core.os.action_spec import ActionSpec


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def make_file_action_spec():
    return ActionSpec(
        action_type="FILE_DELETE",
        category="FILE",
        target="filesystem",
        parameters={},
        risk_level="HIGH",
        required_scopes={"FILE_DELETE"},
        destructive=True,
        supports_undo=True,
        requires_preview=True,
    )


def make_confirmable_pending_action():
    return PendingAction(
        action_spec=make_file_action_spec(),
        preview_data={"path": "/tmp/test.txt"},
        confirmable=True,
    )


# -------------------------------------------------
# Tests
# -------------------------------------------------

def test_no_cancels_pending_action_and_clears_context(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock()
    monkeypatch.setattr(orchestrator, "_dispatch_confirmed_action", spy)

    result = orchestrator.execute(intent=None, args={"raw_text": "no"})

    assert result["type"] in {"deny", "info"}
    assert orchestrator.follow_up_context.pending_action is None
    assert pending.status == "cancelled"
    spy.assert_not_called()


def test_no_with_no_pending_action_is_safe_noop():
    orchestrator = CommandOrchestrator()

    result = orchestrator.execute(intent=None, args={"raw_text": "no"})

    assert result["type"] == "info"


def test_repeated_no_is_idempotent(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock()
    monkeypatch.setattr(orchestrator, "_dispatch_confirmed_action", spy)

    first = orchestrator.execute(intent=None, args={"raw_text": "no"})
    second = orchestrator.execute(intent=None, args={"raw_text": "no"})

    assert first["type"] in {"deny", "info"}
    assert second["type"] == "info"
    assert orchestrator.follow_up_context.pending_action is None
    spy.assert_not_called()


def test_no_does_not_trigger_intent_resolution(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    monkeypatch.setattr(
        orchestrator.follow_up_context,
        "resolve_pending_action",
        MagicMock(side_effect=AssertionError("NLP re-run detected")),
    )

    orchestrator.execute(intent=None, args={"raw_text": "cancel"})


def test_no_never_executes_dispatcher(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock()
    monkeypatch.setattr(orchestrator, "_dispatch_confirmed_action", spy)

    orchestrator.execute(intent=None, args={"raw_text": "stop"})

    spy.assert_not_called()
