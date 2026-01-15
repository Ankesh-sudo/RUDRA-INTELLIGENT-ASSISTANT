from typing import Dict, Optional
from core.nlp.intent import Intent


class PendingAction:
    """
    Holds a partially-resolved command awaiting follow-up input.
    """

    def __init__(self):
        self.intent: Optional[Intent] = None
        self.args: Dict = {}
        self.missing_fields: set[str] = set()

    def set(self, intent: Intent, args: Dict, missing_fields: set[str]):
        self.intent = intent
        self.args = args
        self.missing_fields = missing_fields

    def clear(self):
        self.intent = None
        self.args = {}
        self.missing_fields = set()

    def is_active(self) -> bool:
        return self.intent is not None

    def fill(self, field: str, value):
        self.args[field] = value
        self.missing_fields.discard(field)

    def is_complete(self) -> bool:
        return not self.missing_fields
