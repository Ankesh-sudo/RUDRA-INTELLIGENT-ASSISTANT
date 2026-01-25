import pytest
from core.persona_maturity.persona_freeze import PersonaFreeze


def test_persona_freeze_irreversible():
    PersonaFreeze.freeze()
    assert PersonaFreeze.is_frozen() is True

    # Cannot "unfreeze"
    PersonaFreeze.freeze()
    assert PersonaFreeze.is_frozen() is True


def test_assert_frozen():
    # Already frozen from previous test
    PersonaFreeze.assert_frozen()
