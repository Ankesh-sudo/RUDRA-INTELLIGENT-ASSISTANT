class RecallError(Exception):
    """Base exception for all recall-related errors."""


class InvalidRecallQuery(RecallError):
    """Raised when a recall query is structurally or logically invalid."""


class RecallAccessViolation(RecallError):
    """Raised if recall layer touches write or mutation paths."""
