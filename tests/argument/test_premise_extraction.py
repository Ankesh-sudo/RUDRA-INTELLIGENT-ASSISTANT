import pytest
from core.argument.premise import Premise


def test_valid_premise():
    Premise("Water boils when temperature reaches 100°C").validate()


def test_emotional_premise_rejected():
    with pytest.raises(ValueError):
        Premise("I feel water boils easily").validate()
