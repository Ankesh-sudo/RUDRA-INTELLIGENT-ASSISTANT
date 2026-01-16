from typing import Dict, Optional, Any

from core.nlp.intent import Intent
from core.os.action_spec import ActionSpec


class PendingAction:
    """
    Holds a partially-resolved or confirmation-gated command.

    Day 54 extensions:
    - Supports FILE operations
    - Carries preview data (read-only)
    - Declares undo metadata (no execution)
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
    ):
        # Legacy intent-based follow-ups (Day 15.4 / Day 53)
        self.intent: Optional[Intent] = intent
        self.args: Dict[str, Any] = args or {}
        self.missing_fields: set[str] = missing_fields or set()

        # Day 54: action-based execution
        self.action_spec: Optional[ActionSpec] = action_spec

        # Read-only preview shown to user
        self.preview_data: Optional[Dict[str, Any]] = preview_data

        # Placeholder for Day 55 undo execution
        self.undo_plan: Optional[Dict[str, Any]] = undo_plan

    # -------------------------------------------------
    # Legacy API (DO NOT BREAK)
    # -------------------------------------------------

    def set(self, intent: Intent, args: Dict, missing_fields: set[str]):
        self.intent = intent
        self.args = args
        self.missing_fields = missing_fields

    def clear(self):
        self.intent = None
        self.action_spec = None
        self.args = {}
        self.missing_fields = set()
        self.preview_data = None
        self.undo_plan = None

    def is_active(self) -> bool:
        """
        Active if either:
        - legacy intent follow-up is pending
        - action confirmation is pending
        """
        return self.intent is not None or self.action_spec is not None

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
    # Day 54 helpers (SAFE)
    # -------------------------------------------------

    def requires_confirmation(self) -> bool:
        """
        Whether this pending action is gated by confirmation.
        """
        if self.action_spec:
            return self.action_spec.requires_confirmation
        return False

    def is_file_action(self) -> bool:
        return self.action_spec is not None and self.action_spec.category == "FILE"

    def has_preview(self) -> bool:
        return self.preview_data is not None
