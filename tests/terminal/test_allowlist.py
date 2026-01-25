# tests/terminal/test_allowlist.py

import pytest
from core.terminal.allowlist import is_allowed_command


def test_allowed_commands():
    for cmd in ["ls", "pwd", "whoami", "df", "uptime"]:
        assert is_allowed_command(cmd) is True


def test_disallowed_commands():
    for cmd in ["echo", "cat", "top", "ps", "bash"]:
        assert is_allowed_command(cmd) is False
