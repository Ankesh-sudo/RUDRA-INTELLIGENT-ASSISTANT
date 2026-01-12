import pytest

from core.influence.preferences.lifecycle import PreferenceLifecycleError
from core.influence.preferences.session import PreferenceSession
from core.influence.preferences.types import Preference
from core.influence.preference_scope import PreferenceScope


def _session_scope() -> PreferenceScope:
    """
    Minimal valid scope for lifecycle testing.
    Declarative only.
    """
    scope = PreferenceScope(
        applies_to=frozenset({"output"}),
        contexts=frozenset({"session"}),
        lifetime="session",
        exclusions=frozenset(),
    )
    scope.validate()
    return scope


def test_cannot_apply_without_preview():
    session = PreferenceSession()
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_session_scope(),
    )

    with pytest.raises(PreferenceLifecycleError):
        session.confirm(pref)


def test_cannot_apply_without_confirmation():
    session = PreferenceSession()
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_session_scope(),
    )

    session.preview(pref)
    with pytest.raises(PreferenceLifecycleError):
        session.apply(pref)


def test_valid_preview_confirm_apply_flow():
    session = PreferenceSession()
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_session_scope(),
    )

    session.preview(pref)
    session.confirm(pref)
    assert session.apply(pref) is True
