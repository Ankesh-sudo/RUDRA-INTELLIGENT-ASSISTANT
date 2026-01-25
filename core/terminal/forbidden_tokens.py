# core/terminal/forbidden_tokens.py

from typing import FrozenSet


# Tokens that must NEVER appear in terminal observation specs
# Checked before any parsing or normalization
FORBIDDEN_TOKENS: FrozenSet[str] = frozenset(
    {
        ";",
        "&&",
        "||",
        "|",
        ">",
        ">>",
        "<",
        "$(",
        "`",
        "sudo",
        "su",
        "chmod",
        "chown",
        "rm",
        "mv",
        "cp",
        "dd",
        "mkfs",
        "mount",
        "umount",
    }
)


def contains_forbidden_token(raw_input: str) -> bool:
    """
    Returns True if any forbidden token is present in the raw input.
    Raw string check only — no parsing, no splitting.
    """
    return any(token in raw_input for token in FORBIDDEN_TOKENS)
