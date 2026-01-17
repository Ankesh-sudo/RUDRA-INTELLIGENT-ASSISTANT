# tests/day55/test_file_execution.py

from unittest.mock import MagicMock

from core.orchestrator.command_orchestrator import CommandOrchestrator
from core.context.pending_action import PendingAction
from core.os.action_spec import ActionSpec
from core.os.permission.permission_registry import PermissionRegistry
from core.os.file_ops import file_executor


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

def test_confirmed_file_action_executes_file_executor(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock(return_value={"type": "info"})
    monkeypatch.setattr(file_executor.FileOperationExecutor, "execute", spy)

    result = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    spy.assert_called_once_with(pending)
    assert pending.status == "executed"
    assert orchestrator.follow_up_context.pending_action is None
    assert result["type"] == "info"


def test_file_execution_requires_permission(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    monkeypatch.setattr(
        PermissionRegistry,
        "is_granted",
        MagicMock(return_value=False),
    )

    result = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    assert result["type"] == "permission_denied"
    assert pending.status == "executed"
    assert orchestrator.follow_up_context.pending_action is None


def test_file_executor_not_called_without_confirmation(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock()
    monkeypatch.setattr(file_executor.FileOperationExecutor, "execute", spy)

    orchestrator.execute(intent=None, args={"raw_text": "no"})

    spy.assert_not_called()
    assert orchestrator.follow_up_context.pending_action is None


def test_repeated_yes_does_not_reexecute_file_action(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    spy = MagicMock(return_value={"type": "info"})
    monkeypatch.setattr(file_executor.FileOperationExecutor, "execute", spy)

    first = orchestrator.execute(intent=None, args={"raw_text": "yes"})
    second = orchestrator.execute(intent=None, args={"raw_text": "yes"})

    assert spy.call_count == 1
    assert first["type"] == "info"
    assert second["type"] == "info"


def test_confirmation_never_triggers_nlp_resolution(monkeypatch):
    orchestrator = CommandOrchestrator()

    pending = make_confirmable_pending_action()
    orchestrator.follow_up_context.set_pending_action(pending)

    monkeypatch.setattr(
        orchestrator.follow_up_context,
        "resolve_pending_action",
        MagicMock(side_effect=AssertionError("NLP re-run detected")),
    )

    orchestrator.execute(intent=None, args={"raw_text": "yes"})
