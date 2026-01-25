# tests/terminal/test_spec_validation.py

import pytest

from core.terminal.command_spec import TerminalCommandSpec
from core.terminal.terminal_sandbox import TerminalSandbox
from core.terminal.exceptions import (
    SpecViolationError,
    ForbiddenTokenError,
    AllowListViolationError,
)


def test_valid_command_passes():
    spec = TerminalCommandSpec(
        command="ls",
        args=[],
        reason="Observe directory contents",
    )

    result = TerminalSandbox.validate(spec)

    assert result.command == "ls"
    assert result.read_only is True


def test_empty_command_rejected():
    spec = TerminalCommandSpec(command="")

    with pytest.raises(SpecViolationError):
        TerminalSandbox.validate(spec)


def test_forbidden_token_rejected():
    spec = TerminalCommandSpec(command="ls", args=["&&", "whoami"])

    with pytest.raises(ForbiddenTokenError):
        TerminalSandbox.validate(spec)


def test_allowlist_violation_rejected():
    spec = TerminalCommandSpec(command="echo", args=["hello"])

    with pytest.raises(AllowListViolationError):
        TerminalSandbox.validate(spec)


def test_flags_are_rejected():
    spec = TerminalCommandSpec(command="ls", args=["-la"])

    with pytest.raises(SpecViolationError):
        TerminalSandbox.validate(spec)
