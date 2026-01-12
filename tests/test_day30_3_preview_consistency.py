import pytest

from core.influence.preferences.session import PreferenceSession
from core.influence.preferences.types import Preference
from core.influence.preference_scope import PreferenceScope
from core.influence.preferences.preview import PreferencePreview


def _session_scope() -> PreferenceScope:
    scope = PreferenceScope(
        applies_to=frozenset({"output"}),
        contexts=frozenset({"session"}),
        lifetime="session",
        exclusions=frozenset(),
    )
    scope.validate()
    return scope


def test_consistent_preview_allows_apply():
    session = PreferenceSession(active_context="session")
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_session_scope(),
    )

    preview = PreferencePreview(
        preference=pref,
        preview_text="Use more polite language in responses.",
    )

    session.preview(pref)
    session.confirm(pref)

    assert preview.is_consistent() is True
    assert session.apply(pref, preview=preview) is True


def test_inconsistent_preview_blocks_apply():
    session = PreferenceSession(active_context="session")
    pref = Preference(
        key="tone.polite",
        value=True,
        scope=_session_scope(),
    )

    # Mentions behavior outside language/tone → inconsistent
    preview = PreferencePreview(
        preference=pref,
        preview_text="This will change which commands are executed.",
    )

    session.preview(pref)
    session.confirm(pref)

    assert preview.is_consistent() is False
    assert session.apply(pref, preview=preview) is False
    assert session.is_active(pref) is False
