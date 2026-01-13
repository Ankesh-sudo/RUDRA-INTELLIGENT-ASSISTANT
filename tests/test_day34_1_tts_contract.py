# tests/test_day34_1_tts_contract.py

import pytest

from core.output.tts.tts_contract import (
    FinalizedText,
    TTSContractViolation,
    validate_finalized_text,
)


def test_accepts_raw_string():
    ft = validate_finalized_text("hello world")
    assert isinstance(ft, FinalizedText)
    assert ft.text == "hello world"


def test_accepts_finalized_text():
    original = FinalizedText("ready")
    ft = validate_finalized_text(original)
    assert ft is original


def test_rejects_empty_string():
    with pytest.raises(TTSContractViolation):
        validate_finalized_text("   ")


def test_rejects_non_string():
    with pytest.raises(TTSContractViolation):
        validate_finalized_text(123)


def test_rejects_object_input():
    with pytest.raises(TTSContractViolation):
        validate_finalized_text({"text": "hello"})


def test_finalized_text_is_immutable():
    ft = FinalizedText("immutable")
    with pytest.raises(Exception):
        ft.text = "mutated"
