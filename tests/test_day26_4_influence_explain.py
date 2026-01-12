from core.explain.formatter import format_influence_trace


def test_influence_gate_denied_explanation():
    events = [
        {
            "kind": "memory_influence_gate",
            "decision": "deny",
            "reason": "memory usage mode is DISABLED",
        },
        {
            "kind": "memory_influence_evaluated",
            "result": "skipped",
        },
    ]

    lines = format_influence_trace(events)

    assert len(lines) == 2
    assert "memory influence gate" in lines[0].lower()
    assert "deny" in lines[0].lower()
    assert "disabled" in lines[0].lower()

    assert "evaluated" in lines[1].lower()
    assert "skipped" in lines[1].lower()


def test_influence_allowed_none_applied_explanation():
    events = [
        {
            "kind": "memory_influence_gate",
            "decision": "allow",
            "reason": "memory influence allowed",
        },
        {
            "kind": "memory_influence_evaluated",
            "result": "none_applied",
        },
    ]

    lines = format_influence_trace(events)

    assert len(lines) == 2
    assert "memory influence gate" in lines[0].lower()
    assert "allow" in lines[0].lower()

    assert "none applied" in lines[1].lower()


def test_influence_signals_generated_explanation():
    events = [
        {
            "kind": "memory_influence_gate",
            "decision": "allow",
            "reason": "memory influence allowed",
        },
        {
            "kind": "memory_influence_evaluated",
            "result": "signals_generated",
            "count": 2,
        },
    ]

    lines = format_influence_trace(events)

    assert len(lines) == 2
    assert "2 signals" in lines[1].lower()
