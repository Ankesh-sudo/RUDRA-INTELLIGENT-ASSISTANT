# core/os/file_ops/file_executor.py

"""
Day 55 — Task 3
FileOperationExecutor

Authoritative, isolated executor for CONFIRMED file operations.

Rules (ENFORCED):
- Executes ONLY after confirmation
- No NLP access
- No FollowUpContext access
- No slot filling
- No retries
- Deterministic, testable
"""

import os
from pathlib import Path

from core.context.pending_action import PendingAction
from core.explain.explain_surface import ExplainSurface
from core.os.action_spec import ActionSpec


class FileOperationExecutor:
    """
    Executes confirmed FILE actions.

    Supported operations (Day 55 scope):
    - FILE_DELETE
    """

    @staticmethod
    def execute(pending_action: PendingAction):
        # -------------------------------------------------
        # HARD PRECONDITIONS (NON-NEGOTIABLE)
        # -------------------------------------------------
        if not isinstance(pending_action, PendingAction):
            return ExplainSurface.deny("Invalid pending action")

        if pending_action.status != "executed":
            return ExplainSurface.deny("Action not in executable state")

        spec: ActionSpec = pending_action.action_spec

        if not spec or spec.category != "FILE":
            return ExplainSurface.deny("Unsupported action category")

        # -------------------------------------------------
        # DISPATCH BY ACTION TYPE
        # -------------------------------------------------
        if spec.action_type == "FILE_DELETE":
            return FileOperationExecutor._delete_file(pending_action)

        return ExplainSurface.deny("Unsupported file operation")

    # -------------------------------------------------
    # FILE DELETE (DESTRUCTIVE — CONFIRMED)
    # -------------------------------------------------
    @staticmethod
    def _delete_file(pending_action: PendingAction):
        preview = pending_action.preview_data or {}
        path_str = preview.get("path")

        if not path_str:
            return ExplainSurface.error("Missing file path for deletion")

        try:
            path = Path(path_str).expanduser().resolve()
        except Exception:
            return ExplainSurface.error("Invalid file path")

        # -------------------------------------------------
        # SAFETY CHECKS
        # -------------------------------------------------
        if not path.exists():
            return ExplainSurface.error("File does not exist")

        if not path.is_file():
            return ExplainSurface.error("Target is not a file")

        # Absolute guardrail: never allow root or home deletion
        if path == Path("/") or path == Path.home():
            return ExplainSurface.deny("Protected path deletion blocked")

        # -------------------------------------------------
        # EXECUTION (POINT OF NO RETURN)
        # -------------------------------------------------
        try:
            os.remove(path)
        except PermissionError:
            return ExplainSurface.permission_denied("FILE_DELETE")
        except Exception as e:
            return ExplainSurface.error(f"File deletion failed: {e}")

        # -------------------------------------------------
        # SUCCESS SURFACE
        # -------------------------------------------------
        return ExplainSurface.info(
            "File deleted successfully",
            payload={
                "operation": "FILE_DELETE",
                "path": str(path),
                "supports_undo": pending_action.action_spec.supports_undo,
            },
        )
