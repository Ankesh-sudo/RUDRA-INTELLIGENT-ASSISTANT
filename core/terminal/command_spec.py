# core/terminal/command_spec.py

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class TerminalCommandSpec:
    """
    Immutable specification for a terminal observation command.

    This object is PURE DATA.
    - No execution
    - No parsing
    - No OS interaction
    """

    command: str
    args: List[str] = field(default_factory=list)
    reason: str = ""
    read_only: bool = True
    source: str = "terminal_observation"

    def full_command(self) -> List[str]:
        """
        Returns the command as an argv-style list.
        """
        return [self.command, *self.args]
