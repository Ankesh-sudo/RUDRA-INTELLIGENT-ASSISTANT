# tests/test_day36_1_persona_profile_immutable.py

import pytest
from dataclasses import FrozenInstanceError

from core.persona.profile import PersonaProfile


def test_persona_profile_is_immutable():
    profile = PersonaProfile(
        name="Maahi",
        version="1.0",
        affection_tier="A",
        suffixes=(" 🙂", " Boss 😊"),
    )

    # Attempt to mutate a field
    with pytest.raises(FrozenInstanceError):
        profile.name = "EvilMaahi"


def test_persona_suffixes_are_immutable():
    profile = PersonaProfile(
        name="Maahi",
        version="1.0",
        affection_tier="A",
        suffixes=(" 🙂", " Boss 😊"),
    )

    # Tuples are immutable; reassignment should fail
    with pytest.raises(FrozenInstanceError):
        profile.suffixes += (" hacked",)
