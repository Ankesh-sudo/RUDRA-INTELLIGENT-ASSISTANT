from core.explain.formatter import explain_last


def test_empty_trace():
    assert explain_last([]) == []


def test_preference_blocked_shows_no_effect():
    trace = [
        {"kind": "output_preference_blocked", "reason": "disabled"},
    ]

    out = explain_last(trace)
    assert "Output preferences blocked: disabled" in out
    assert "No output preferences affected the response." in out


def test_opt_out_explained():
    trace = [
        {"kind": "output_preference_opt_out"},
    ]

    out = explain_last(trace)
    assert "Output preference usage disabled by user" in out
    assert "No output preferences affected the response." in out


def test_expiry_explained():
    trace = [
        {"kind": "output_preference_session_expired"},
    ]

    out = explain_last(trace)
    assert "Output preference usage expired at session end" in out


def test_preference_applied_no_no_effect_line():
    trace = [
        {
            "kind": "output_preference_applied",
            "key": "verbosity",
            "value": "short",
        }
    ]

    out = explain_last(trace)
    assert "Output preference applied: verbosity = short" in " ".join(out)
    assert "No output preferences affected the response." not in out
