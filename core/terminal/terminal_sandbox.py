# core/terminal/terminal_sandbox.py

from dataclasses import dataclass
from typing import List

from core.terminal.command_spec import TerminalCommandSpec
from core.terminal.allowlist import is_allowed_command
from core.terminal.forbidden_tokens import contains_forbidden_token
from core.terminal.output_limits import OutputLimits
from core.terminal.exceptions import (
    SpecViolationError,
    ForbiddenTokenError,
    AllowListViolationError,
)


@dataclass(frozen=True)
class ValidationResult:
    """
    Result of terminal specification validation.

    This is a declarative outcome:
    - No execution
    - No OS interaction
    """

    command: str
    args: List[str]
    reason: str
    output_limits: OutputLimits
    timeout_seconds: int
    read_only: bool


class TerminalSandbox:
    """
    Parse-only terminal validation sandbox.

    Responsibilities:
    - Enforce allow-list
    - Detect forbidden tokens
    - Ensure read-only semantics
    - Declare output and timeout constraints

    ABSOLUTELY NO EXECUTION.
    """

    DEFAULT_TIMEOUT_SECONDS = 3

    @staticmethod
    def validate(spec: TerminalCommandSpec) -> ValidationResult:
        if not isinstance(spec, TerminalCommandSpec):
            raise SpecViolationError("Invalid terminal command specification type")

        if not spec.command:
            raise SpecViolationError("Command cannot be empty")

        if not spec.read_only:
            raise SpecViolationError("Terminal command must be read-only")

        # Raw token scan (command + args)
        raw_input = " ".join([spec.command, *spec.args])

        if contains_forbidden_token(raw_input):
            raise ForbiddenTokenError(
                f"Forbidden token detected in terminal input: '{raw_input}'"
            )

        # Allow-list enforcement
        if not is_allowed_command(spec.command):
            raise AllowListViolationError(
                f"Command '{spec.command}' is not in the terminal allow-list"
            )

        # Argument sanity (no flags or switches allowed)
        for arg in spec.args:
            if arg.startswith("-"):
                raise SpecViolationError(
                    f"Flags are not permitted in terminal observation commands: '{arg}'"
                )

        # Declarative output limits
        output_limits = OutputLimits()

        return ValidationResult(
            command=spec.command,
            args=list(spec.args),
            reason=spec.reason,
            output_limits=output_limits,
            timeout_seconds=TerminalSandbox.DEFAULT_TIMEOUT_SECONDS,
            read_only=True,
        )
