# tests/test_intent_splitter.py

import pytest

from core.intelligence.intent_splitter import IntentSplitter


def test_multi_command_split():
    text = "open chrome and search instagram then open login page"
    parts = IntentSplitter().split(text)
    assert parts == [
        "open chrome",
        "search instagram",
        "open login page",
    ]


def test_split_with_after_that():
    text = "open chrome after that search instagram"
    parts = IntentSplitter().split(text)
    assert parts == [
        "open chrome",
        "search instagram",
    ]


def test_split_with_next():
    text = "open chrome next search instagram"
    parts = IntentSplitter().split(text)
    assert parts == [
        "open chrome",
        "search instagram",
    ]


def test_split_preserves_order_and_trims_spaces():
    text = "  open chrome   and   search instagram   "
    parts = IntentSplitter().split(text)
    assert parts == [
        "open chrome",
        "search instagram",
    ]


def test_single_command_no_split():
    text = "open chrome"
    parts = IntentSplitter().split(text)
    assert parts == ["open chrome"]


def test_empty_input_returns_empty_list():
    text = "   "
    parts = IntentSplitter().split(text)
    assert parts == []
