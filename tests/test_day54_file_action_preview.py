import os
import tempfile

import pytest

from core.skills import file_actions
from core.context.pending_action import PendingAction
from core.explain.explain_surface import ExplainSurface
from core.nlp.intent import Intent
from core.os.action_spec import ActionSpec
from core.os.permission.permission_registry import PermissionRegistry


# -------------------------------------------------
# Fixtures
# -------------------------------------------------

@pytest.fixture
def temp_file(tmp_path):
    """
    Create a temporary file inside HOME sandbox.
    """
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    return file_path


@pytest.fixture
def delete_command_text(temp_file):
    return f"delete {temp_file.name}"


# -------------------------------------------------
# Tests
# -------------------------------------------------

def test_delete_file_creates_pending_action_only(monkeypatch, temp_file, delete_command_text):
    """
    Ensure delete command:
    - creates PendingAction
    - does NOT delete file
    - includes preview
    """

    # Force HOME_DIR sandbox to tmp_path
    monkeypatch.setattr(
        "core.system.path_resolver.HOME_DIR",
        str(temp_file.parent),
    )

    result = file_actions.handle(Intent.DELETE_FILE, delete_command_text)

    assert result is not None, "Handler returned None"

    pending, explain = result

    # ---- type checks ----
    assert isinstance(pending, PendingAction)
    assert isinstance(explain, ExplainSurface)

    # ---- action spec ----
    assert pending.action_spec is not None
    assert isinstance(pending.action_spec, ActionSpec)
    assert pending.action_spec.action_type == "DELETE_FILE"
    assert pending.action_spec.requires_confirmation is True
    assert pending.action_spec.destructive is True
    # NOTE: required_scopes may be empty on Day 54

    # ---- preview ----
    assert pending.preview_data is not None
    assert pending.preview_data["path"].endswith("test.txt")
    assert pending.preview_data["type"] == "file"
    assert "size" in pending.preview_data

    # ---- filesystem safety ----
    assert os.path.exists(temp_file), "File was deleted (NOT ALLOWED on Day 54)"


def test_delete_file_requires_confirmation():
    """
    Confirm delete actions are confirmation-gated.
    """
    action = ActionSpec(
        action_type="DELETE_FILE",
        category="FILE",
        target="/tmp/x.txt",
        parameters={},
        risk_level="HIGH",
        required_scopes=PermissionRegistry.get_required_scopes("DELETE_FILE"),
        destructive=True,
        supports_undo=True,
        requires_preview=True,
    )

    assert action.requires_confirmation is True


def test_yes_does_not_execute_file_deletion(monkeypatch, temp_file):
    """
    Simulate user saying 'yes'.
    On Day 54, this MUST NOT execute deletion.
    """

    monkeypatch.setattr(
        "core.system.path_resolver.HOME_DIR",
        str(temp_file.parent),
    )

    result = file_actions.handle(
        Intent.DELETE_FILE,
        f"delete {temp_file.name}",
    )

    pending, _ = result

    assert pending.requires_confirmation() is True

    # Simulated "yes" (no executor yet)
    assert os.path.exists(temp_file), "File was deleted after 'yes' (NOT ALLOWED on Day 54)"


def test_missing_file_returns_explain_only(monkeypatch):
    """
    Deleting a non-existent file should return explanation only.
    """

    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(
            "core.system.path_resolver.HOME_DIR",
            tmp,
        )

        result = file_actions.handle(
            Intent.DELETE_FILE,
            "delete ghost.txt",
        )

        assert isinstance(result, ExplainSurface)
