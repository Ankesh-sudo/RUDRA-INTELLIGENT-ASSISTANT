from core.influence.preference_scope import PreferenceScope
from core.influence.preference_resolution import ResolvedPreference
from core.influence.preference_preview import build_previews
from core.influence.preference_confirmation import PreferenceConfirmation


def scope_for(contexts):
    return PreferenceScope(
        applies_to=frozenset({"output_text"}),
        contexts=frozenset(contexts),
        lifetime="session",
        exclusions=frozenset(),
    )


def test_preview_filters_by_context():
    resolved = {
        "verbosity": ResolvedPreference(
            key="verbosity",
            value="short",
            weight=0.2,
            scope=scope_for({"normal_reply"}),
        )
    }

    previews = build_previews(resolved, context="normal_reply")
    assert len(previews) == 1

    previews_none = build_previews(resolved, context="clarification")
    assert previews_none == []


def test_confirmation_flow():
    conf = PreferenceConfirmation()
    conf.confirm(["verbosity"])
    assert "verbosity" in conf.confirmed_keys()

    conf.reject(["verbosity"])
    assert "verbosity" not in conf.confirmed_keys()


def test_clear_resets_session():
    conf = PreferenceConfirmation()
    conf.confirm(["verbosity"])
    conf.clear()
    assert conf.confirmed_keys() == set()
