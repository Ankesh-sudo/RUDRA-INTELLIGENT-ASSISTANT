# core/terminal/exceptions.py

class TerminalSpecError(Exception):
    """
    Base class for all terminal specification validation errors.
    All subclasses must be explainable and deterministic.
    """
    pass


class SpecViolationError(TerminalSpecError):
    """
    Raised when a TerminalCommandSpec violates structural
    or semantic constraints.
    """
    pass


class ForbiddenTokenError(TerminalSpecError):
    """
    Raised when forbidden tokens are detected in raw input
    or command arguments.
    """
    pass


class AllowListViolationError(TerminalSpecError):
    """
    Raised when a command is not present in the terminal allow-list.
    """
    pass
