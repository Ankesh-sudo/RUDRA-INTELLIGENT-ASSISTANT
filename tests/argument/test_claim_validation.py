import pytest
from core.argument.claim import Claim


def test_valid_claim():
    Claim("Water boils at 100 degrees Celsius").validate()


def test_empty_claim():
    with pytest.raises(ValueError):
        Claim("").validate()


def test_question_claim():
    with pytest.raises(ValueError):
        Claim("Is water wet?").validate()
