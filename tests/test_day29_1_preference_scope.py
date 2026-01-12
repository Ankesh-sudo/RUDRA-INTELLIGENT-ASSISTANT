import pytest

from core.influence.preference_scope import PreferenceScope
from core.influence.preference_resolution import ResolvedPreference


def valid_scope():
    return PreferenceScope(
        applies_to=frozenset({"output_text"}),
        contexts=frozenset({"normal_reply"}),
        lifetime="session",
        exclusions=frozenset({"error_messages"}),
    )


def test_scope_validates_successfully():
    valid_scope().validate()


def test_scope_missing_lifetime_rejected():
    with pytest.raises(ValueError):
        PreferenceScope(
            applies_to=frozenset({"output_text"}),
            contexts=frozenset({"normal_reply"}),
            lifetime="",
            exclusions=frozenset(),
        ).validate()


def test_scope_requires_frozenset_fields():
    with pytest.raises(ValueError):
        PreferenceScope(
            applies_to={"output_text"},  # wrong type
            contexts=frozenset(),
            lifetime="session",
            exclusions=frozenset(),
        ).validate()


def test_resolved_preference_requires_scope():
    with pytest.raises(TypeError):
        ResolvedPreference(
            key="verbosity",
            value="short",
            weight=0.2,
        )


def test_scope_is_immutable():
    scope = valid_scope()
    with pytest.raises(Exception):
        scope.applies_to.add("explain_only")
