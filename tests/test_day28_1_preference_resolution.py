from core.influence.preference_resolver import resolve_preferences


def pref(key, value, source, ts):
    return {
        "key": key,
        "value": value,
        "source": source,
        "timestamp": ts,
    }


def test_single_preference():
    result = resolve_preferences(
        detected_preferences=[],
        session_preferences=[pref("verbosity", "short", "session", 10)],
        scoped_preferences=[],
        stored_preferences=[],
    )

    assert result.get("verbosity").value == "short"
    assert result.get("verbosity").source == "session"


def test_priority_resolution():
    result = resolve_preferences(
        detected_preferences=[],
        session_preferences=[pref("tone", "casual", "session", 5)],
        scoped_preferences=[pref("tone", "formal", "scoped", 10)],
        stored_preferences=[pref("tone", "neutral", "stored", 20)],
    )

    assert result.get("tone").value == "casual"
    assert result.get("tone").source == "session"


def test_timestamp_resolution_same_source():
    result = resolve_preferences(
        detected_preferences=[],
        session_preferences=[
            pref("format", "bullet", "session", 10),
            pref("format", "paragraph", "session", 20),
        ],
        scoped_preferences=[],
        stored_preferences=[],
    )

    assert result.get("format").value == "paragraph"


def test_empty_inputs():
    result = resolve_preferences([], [], [], [])
    assert result.is_empty()


def test_deterministic_key_ordering():
    result = resolve_preferences(
        detected_preferences=[],
        session_preferences=[
            pref("b", "x", "session", 1),
            pref("a", "y", "session", 1),
        ],
        scoped_preferences=[],
        stored_preferences=[],
    )

    assert result.keys() == ["a", "b"]


def test_explain_rejected_preferences():
    result = resolve_preferences(
        detected_preferences=[],
        session_preferences=[pref("verbosity", "short", "session", 5)],
        scoped_preferences=[pref("verbosity", "long", "scoped", 10)],
        stored_preferences=[],
    )

    record = result.get("verbosity")
    assert len(record.rejected) == 1
    assert record.rejected[0]["source"] == "scoped"
