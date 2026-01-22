import re
from typing import Optional

from core.nlp.intent import Intent
from core.context.pending_action import PendingAction
from core.explain.explain_surface import ExplainSurface
from core.os.action_spec import ActionSpec
from core.os.permission.permission_registry import PermissionRegistry
from core.system.path_resolver import (
    resolve_base_path,
    resolve_file_path,
    build_path_preview,
)


def handle(intent: Intent, raw_text: str):
    text = raw_text.lower().strip()

    if intent == Intent.DELETE_FILE:
        return _prepare_delete(text)

    if intent == Intent.COPY_FILE:
        return _explain_only("Copy will be enabled on Day 55.")

    if intent == Intent.MOVE_FILE:
        return _explain_only("Move will be enabled on Day 55.")

    return None


def _prepare_delete(text: str):
    filename = _extract_filename(text)
    if not filename:
        return _explain_only("Please specify the file to delete.")

    base_dir = resolve_base_path(text)
    if not base_dir:
        return _explain_only("I can't access that location.")

    source_path = resolve_file_path(filename, base_dir)
    if not source_path:
        return _explain_only("That file does not exist.")

    preview = build_path_preview(source_path)
    if not preview:
        return _explain_only("That file does not exist.")

    # -------------------------------------------------
    # ActionSpec — ONLY supported + legacy fields
    # -------------------------------------------------
    action_spec = ActionSpec(
        action_type="DELETE_FILE",
        risk_level="HIGH",
        required_scopes=PermissionRegistry.get_required_scopes("DELETE_FILE"),
        destructive=True,  # ✅ LEGACY FIELD (allowed)
    )

    pending = PendingAction(
        action_spec=action_spec,
        preview_data=preview,
        undo_plan=None,
        confirmable=True,  # ✅ confirmation handled HERE
    )

    explain = ExplainSurface.from_lines(
        "I’m about to delete:",
        f"📄 {preview['path']}",
        "",
        "Should I proceed?",
    )

    return pending, explain


def _extract_filename(text: str) -> Optional[str]:
    match = re.search(r"\b([\w\-]+\.[a-z0-9]+)\b", text)
    return match.group(1) if match else None


def _explain_only(message: str):
    return ExplainSurface.from_lines(message)
