# core/terminal/dry_run_preview.py

from dataclasses import dataclass
from core.terminal.command_spec import TerminalCommandSpec


@dataclass(frozen=True)
class DryRunPreview:
    """
    Human-readable dry-run preview.
    No execution. No side effects.
    """

    command: str
    args: list[str]
    why_allowed: str
    what_will_be_observed: str

    def render(self) -> str:
        return (
            f"Command: {self.command} {' '.join(self.args)}\n"
            f"Allowed because: {self.why_allowed}\n"
            f"Observation: {self.what_will_be_observed}"
        )
