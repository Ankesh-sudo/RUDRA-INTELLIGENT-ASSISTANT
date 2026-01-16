from unittest.mock import MagicMock

from core.orchestrator.command_orchestrator import CommandOrchestrator
from core.context.pending_action import PendingAction
from core.os.action_spec import ActionSpec
from core.os.permission.scopes import FILE_DELETE


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def make_file_action_spec():
    """
    Fully valid destructive FILE DELETE action.
    """
    return ActionSpec(
        action_type=FILE_DELETE,     # ✅ FIX
        category="FILE",
        target="filesystem",
        parameters={},
        risk_level="HIGH",
        required_scopes={FILE_DELETE},
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

def test_yes_with_valid_pending_action_executes_dispatcher(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock(return_value={"type": "info"})
    monkeypatch.setattr(orchestrator, "_dispatch_confirmed_action", spy)

    result = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    spy.assert_called_once_with(pending)
    assert result["type"] == "info"
    assert orchestrator.follow_up_context.pending_action is None
    assert pending.status == "executed"


def test_yes_with_no_pending_action_is_safe_noop():
    orchestrator = CommandOrchestrator()

    result = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    assert result["type"] == "info"


def test_yes_with_non_confirmable_pending_action_denied():
    orchestrator = CommandOrchestrator()

    pending = PendingAction(
        action_spec=make_file_action_spec(),
        preview_data={"path": "/tmp/test.txt"},
        confirmable=False,
    )
    orchestrator.follow_up_context.set_pending_action(pending)

    result = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    assert result["type"] == "deny"
    assert pending.status == "awaiting_confirmation"


def test_yes_after_already_executed_pending_action_denied():
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    pending.status = "executed"
    orchestrator.follow_up_context.set_pending_action(pending)

    result = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    assert result["type"] == "deny"


def test_repeated_yes_does_not_reexecute(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock(return_value={"type": "info"})
    monkeypatch.setattr(orchestrator, "_dispatch_confirmed_action", spy)

    first = orchestrator.execute(intent=None, args={"raw_text": "yes"})
    second = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    assert spy.call_count == 1
    assert first["type"] == "info"
    assert second["type"] == "info"


def test_confirmation_does_not_trigger_intent_resolution(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    monkeypatch.setattr(
        orchestrator.follow_up_context,
        "resolve_pending_action",
        MagicMock(side_effect=AssertionError("NLP re-run detected")),
    )

    orchestrator.execute(intent=None, args={"raw_text": "yes"})
