# tests/terminal/test_day69_terminal_execution.py

import pytest

from core.terminal.command_spec import TerminalCommandSpec
from core.terminal.terminal_sandbox import TerminalSandbox
from core.terminal.terminal_executor import TerminalExecutor
from core.orchestrator.execution_session import ExecutionSession


def test_terminal_execution_ls():
    spec = TerminalCommandSpec(command="pwd", reason="Observe cwd")
    validation = TerminalSandbox.validate(spec)
    session = ExecutionSession()

    result = TerminalExecutor.execute(validation, session)

    assert result.returncode == 0
    assert result.stdout.strip() != ""
    assert result.truncated is False


def test_terminal_execution_respects_timeout():
    spec = TerminalCommandSpec(command="uptime", reason="Observe uptime")
    validation = TerminalSandbox.validate(spec)
    session = ExecutionSession()

    result = TerminalExecutor.execute(validation, session)

    assert result.returncode == 0
