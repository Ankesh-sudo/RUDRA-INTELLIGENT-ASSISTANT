from typing import List


def format_core_trace(events: list) -> List[str]:
    """
    Formats core (non-memory) trace events.
    Pure presentation only.
    """
    lines = []

    for e in events:
        kind = e.get("kind")

        if kind == "intent_selected":
            lines.append(f"Intent selected: {e.get('intent')}")

        elif kind == "action_executed":
            lines.append(f"Action executed: {e.get('action')}")

    return lines


def format_memory_trace(events: list) -> List[str]:
    """
    Formats memory recall and usage traces.
    Pure presentation only.
    """
    lines = []

    for e in events:
        kind = e.get("kind")

        if kind == "memory_recall":
            lines.append(
                f"Memory recall: {e.get('count', 0)} entries returned"
            )

        elif kind == "memory_usage":
            lines.append(
                f"Memory usage mode: {e.get('mode')}"
            )

    return lines


def format_influence_trace(events: list) -> List[str]:
    """
    Formats memory influence evaluation traces.
    Pure formatter — no logic, no inference.
    """
    lines = []

    for e in events:
        kind = e.get("kind")

        if kind == "memory_influence_gate":
            lines.append(
                f"Memory influence gate: {e.get('decision')} ({e.get('reason')})"
            )

        elif kind == "memory_influence_evaluated":
            result = e.get("result")

            if result == "skipped":
                lines.append(
                    "Memory influence evaluated: skipped (gate denied)"
                )
            elif result == "none_applied":
                lines.append(
                    "Memory influence evaluated: none applied"
                )
            else:
                lines.append(
                    f"Memory influence evaluated: {e.get('count', 0)} signals generated"
                )

    return lines


def explain_last(trace_events: list) -> List[str]:
    """
    Explains the most recent assistant response.
    """
    output: List[str] = []

    output.extend(format_core_trace(trace_events))
    output.extend(format_memory_trace(trace_events))
    output.extend(format_influence_trace(trace_events))

    return output


def explain_all(trace_events: list) -> List[str]:
    """
    Explains all assistant decisions in the session.
    """
    output: List[str] = []

    output.extend(format_core_trace(trace_events))
    output.extend(format_memory_trace(trace_events))
    output.extend(format_influence_trace(trace_events))

    return output
