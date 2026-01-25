# core/terminal/allowlist.py

from typing import FrozenSet


# Hard, immutable allow-list for terminal observation
# No flags, no mutations, no expansion
ALLOWED_COMMANDS: FrozenSet[str] = frozenset(
    {
        "ls",
        "pwd",
        "whoami",
        "df",
        "uptime",
    }
)


def is_allowed_command(command: str) -> bool:
    """
    Check whether a command is explicitly allowed.

    No normalization or fallback logic is performed here.
    """
    return command in ALLOWED_COMMANDS
