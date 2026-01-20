from typing import Any, Set
from core.os.action_spec import ActionSpec


class PlannedAction:
    """
    Planned (but not executed) action derived from an intent.
    """
    def __init__(
        self,
        action_spec: ActionSpec,
        source_intent: Any,
        dependencies: Set["PlannedAction"] | None = None,
    ):
        self.action_spec = action_spec
        self.source_intent = source_intent
        self.dependencies = dependencies or set()

    def __repr__(self) -> str:
        return f"<PlannedAction {self.action_spec.action}>"
