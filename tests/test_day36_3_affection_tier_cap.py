# tests/test_day36_3_affection_tier_cap.py

import pytest

from core.persona.profile import PersonaProfile
from core.persona.persona_lock import PersonaLock


def test_affection_tier_a_is_allowed():
    profile = PersonaProfile(
        name="Maahi",
        version="1.0",
        affection_tier="A",
        suffixes=(" 🙂",),
    )

    # Should not raise
    PersonaLock.validate(profile)


def test_affection_tier_escalation_is_blocked():
    profile = PersonaProfile(
        name="Maahi",
        version="1.0",
        affection_tier="B",  # illegal
        suffixes=(" ❤️",),
    )

    with pytest.raises(RuntimeError):
        PersonaLock.validate(profile)
