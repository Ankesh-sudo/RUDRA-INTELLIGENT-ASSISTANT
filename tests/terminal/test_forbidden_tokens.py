# tests/terminal/test_forbidden_tokens.py

from core.terminal.forbidden_tokens import contains_forbidden_token


def test_detects_forbidden_tokens():
    assert contains_forbidden_token("ls && whoami")
    assert contains_forbidden_token("pwd | grep home")
    assert contains_forbidden_token("sudo ls")
    assert contains_forbidden_token("echo $(whoami)")


def test_allows_clean_input():
    assert not contains_forbidden_token("ls")
    assert not contains_forbidden_token("pwd home")
