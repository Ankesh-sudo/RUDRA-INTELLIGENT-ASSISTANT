import subprocess
from dataclasses import dataclass
from typing import List

from core.orchestrator.execution_session import ExecutionSession
from core.terminal.terminal_sandbox import ValidationResult
from core.terminal.exceptions import SpecViolationError


@dataclass(frozen=True)
class TerminalExecutionResult:
    """
    Result of a controlled terminal execution.
    Read-only, no shell, bounded output.
    """
    command: List[str]
    stdout: str
    stderr: str
    returncode: int
    truncated: bool


class TerminalExecutor:
    """
    Controlled execution backend for terminal observation.

    Guarantees:
    - subprocess.run only
    - shell=False
    - allow-list enforced earlier
    - session abort respected
    """

    @staticmethod
    def execute(
        validation: ValidationResult,
        session: ExecutionSession,
    ) -> TerminalExecutionResult:

        if not validation.read_only:
            raise SpecViolationError("Execution denied: non read-only command")

        if session.abort_requested:
            raise SpecViolationError("Execution aborted: session cancelled")

        try:
            completed = subprocess.run(
                [validation.command, *validation.args],
                capture_output=True,
                text=True,
                timeout=validation.timeout_seconds,
                shell=False,
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise SpecViolationError("Execution aborted: timeout")

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        truncated = False
        max_bytes = validation.output_limits.max_bytes

        if len(stdout.encode()) > max_bytes:
            stdout = stdout.encode()[:max_bytes].decode(errors="ignore")
            truncated = True

        # DAY 69 — observation attachment (read-only)
        session.attach_observation("terminal", validation.command)

        return TerminalExecutionResult(
            command=[validation.command, *validation.args],
            stdout=stdout,
            stderr=stderr,
            returncode=completed.returncode,
            truncated=truncated,
        )
