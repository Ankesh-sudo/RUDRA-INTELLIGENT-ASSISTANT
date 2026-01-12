import pytest

from core.influence.preferences.session import PreferenceSession
from core.influence.preferences.types import Preference
from core.influence.preference_scope import PreferenceScope


def _once_scope() -> PreferenceScope:
    scope = PreferenceScope(
        applies_to=frozenset({"output"}),
        contexts=frozenset({"session"}),
        lifetime="once",
        exclusions=frozenset(),
    )
    scope.validate()
    return scope


def _session_scope() -> PreferenceScope:
    scope = PreferenceScope(
        applies_to=frozenset({"output"}),
        contexts=frozenset({"session"}),
        lifetime="session",
        exclusions=frozenset(),
    )
    scope.validate()
    return scope


def _other_context_scope() -> PreferenceScope:
    scope = PreferenceScope(
        applies_to=frozenset({"output"}),
        contexts=frozenset({"other_context"}),
        lifetime="session",
        exclusions=frozenset(),
    )
    scope.validate()
    return scope


def test_once_lifetime_expires_after_apply():
    session = PreferenceSession(active_context="session")
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_once_scope(),
    )

    session.preview(pref)
    session.confirm(pref)
    assert session.apply(pref) is True

    # must be expired immediately after use
    assert session.is_active(pref) is False


def test_session_lifetime_remains_active():
    session = PreferenceSession(active_context="session")
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_session_scope(),
    )

    session.preview(pref)
    session.confirm(pref)
    assert session.apply(pref) is True
    assert session.is_active(pref) is True


def test_context_mismatch_results_in_noop():
    session = PreferenceSession(active_context="session")
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_other_context_scope(),
    )

    session.preview(pref)
    session.confirm(pref)

    # no error, but no application
    assert session.apply(pref) is False
    assert session.is_active(pref) is False
