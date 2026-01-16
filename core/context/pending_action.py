from __future__ import annotations

from typing import Dict, Optional, Any, Literal
from datetime import datetime
import uuid

from core.nlp.intent import Intent
from core.os.action_spec import ActionSpec


class PendingAction:
    """
    Holds a partially-resolved or confirmation-gated command.

    Guarantees:
    - No inference
    - No execution
    - No permission logic
    - No mutation

    Used by:
    - Legacy intent follow-ups (Day 15.4)
    - Action confirmation flow (Day 54 → Day 55)
    """

    def __init__(
        self,
        *,
        intent: Optional[Intent] = None,
        action_spec: Optional[ActionSpec] = None,
        args: Optional[Dict[str, Any]] = None,
        missing_fields: Optional[set[str]] = None,
        preview_data: Optional[Dict[str, Any]] = None,
        undo_plan: Optional[Dict[str, Any]] = None,
        confirmable: bool = False,
    ):
        # ---- Identity & lifecycle ----
        self.id: str = str(uuid.uuid4())
        self.created_at: datetime = datetime.utcnow()
        self.status: Literal[
            "awaiting_confirmation", "executed", "cancelled"
        ] = "awaiting_confirmation"

        # ---- Legacy intent-based follow-ups ----
        self.intent: Optional[Intent] = intent
        self.args: Dict[str, Any] = args or {}
        self.missing_fields: set[str] = missing_fields or set()

        # ---- Action-based execution (Day 54+) ----
        self.action_spec: Optional[ActionSpec] = action_spec
        self.confirmable: bool = confirmable

        # Immutable preview payload (authoritative execution input)
        self.preview_data: Optional[Dict[str, Any]] = preview_data

        # Placeholder for undo metadata (execution happens later)
        self.undo_plan: Optional[Dict[str, Any]] = undo_plan

    # -------------------------------------------------
    # Legacy API (DO NOT BREAK)
    # -------------------------------------------------

    def set(self, intent: Intent, args: Dict, missing_fields: set[str]):
        self.intent = intent
        self.args = args
        self.missing_fields = missing_fields

    def clear(self):
        """
        Hard reset. Used only when abandoning pending state.
        """
        self.intent = None
        self.action_spec = None
        self.args = {}
        self.missing_fields = set()
        self.preview_data = None
        self.undo_plan = None
        self.confirmable = False
        self.status = "cancelled"

    def is_active(self) -> bool:
        """
        Active if either:
        - legacy intent follow-up is pending
        - action confirmation is pending
        """
        return (
            self.status == "awaiting_confirmation"
            and (self.intent is not None or self.action_spec is not None)
        )

    def fill(self, field: str, value):
        """
        Used only for legacy slot completion.
        File actions do NOT use this.
        """
        self.args[field] = value
        self.missing_fields.discard(field)

    def is_complete(self) -> bool:
        """
        Legacy completion check.
        """
        return not self.missing_fields

    # -------------------------------------------------
    # Day 54–55 helpers (AUTHORITATIVE)
    # -------------------------------------------------

    def requires_confirmation(self) -> bool:
        """
        Whether this pending action is gated by confirmation.
        """
        return bool(self.confirmable)

    def is_confirmable(self) -> bool:
        """
        Single authoritative check used by orchestrator.
        """
        return (
            self.confirmable
            and self.status == "awaiting_confirmation"
            and self.action_spec is not None
            and self.preview_data is not None
        )

    def is_file_action(self) -> bool:
        return self.action_spec is not None and self.action_spec.category == "FILE"

    def has_preview(self) -> bool:
        return self.preview_data is not None

    # -------------------------------------------------
    # Lifecycle transitions (SINGLE-USE)
    # -------------------------------------------------

    def mark_executed(self):
        if self.status != "awaiting_confirmation":
            raise RuntimeError("PendingAction already consumed")
        self.status = "executed"

    def mark_cancelled(self):
        if self.status != "awaiting_confirmation":
            return
        self.status = "cancelled"
