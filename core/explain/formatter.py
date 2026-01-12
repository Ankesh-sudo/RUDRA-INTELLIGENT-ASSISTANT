from typing import List, Optional

from core.influence.output_preferences import OutputPreferences
from core.influence.preference_scope import PreferenceScope
from core.influence.preference_preview import PreferencePreview


# ---------- Core Formatting ----------

def format_core_trace(events: list) -> List[str]:
    lines: List[str] = []

    for e in events:
        if e.get("kind") == "intent_selected":
            lines.append(f"Intent selected: {e.get('intent')}")
        elif e.get("kind") == "action_executed":
            lines.append(f"Action executed: {e.get('action')}")

    return lines


def format_memory_trace(events: list) -> List[str]:
    lines: List[str] = []

    for e in events:
        if e.get("kind") == "memory_recall":
            lines.append(
                f"Memory recall: {e.get('count', 0)} entries returned"
            )
        elif e.get("kind") == "memory_usage":
            lines.append(
                f"Memory usage mode: {e.get('mode')}"
            )

    return lines


# ---------- Preference Scope Formatting (Day 29.1) ----------

def _format_scope(scope: PreferenceScope) -> List[str]:
    return [
        "  Scope:",
        f"    Applies to: {', '.join(sorted(scope.applies_to)) or '—'}",
        f"    Contexts: {', '.join(sorted(scope.contexts)) or '—'}",
        f"    Lifetime: {scope.lifetime}",
        f"    Exclusions: {', '.join(sorted(scope.exclusions)) or '—'}",
    ]


# ---------- Preference Preview Formatting (Day 29.2) ----------

def _format_previews(previews: List[PreferencePreview]) -> List[str]:
    lines: List[str] = ["Preference preview:"]

    if not previews:
        lines.append("- (none)")
        return lines

    for p in previews:
        lines.append(
            f"- {p.key}={p.value} ({p.effect})"
        )

    return lines


# ---------- Influence + Preference Formatting ----------

def format_influence_trace(events: list) -> List[str]:
    """
    Deterministic, linear explain surface for all influence & preference events.
    """
    lines: List[str] = []

    applied_any = False
    preference_system_seen = False
    preview_seen = False
    confirmation_seen = False

    # ---- 1. Memory influence gating / evaluation ----
    for e in events:
        kind = e.get("kind")

        if kind == "memory_influence_gate":
            lines.append(
                f"Memory influence gate: {e.get('decision')} ({e.get('reason')})"
            )

        elif kind == "memory_influence_evaluated":
            result = e.get("result")

            if result == "skipped":
                lines.append("Memory influence evaluated: skipped (gate denied)")
            elif result == "none_applied":
                lines.append("Memory influence evaluated: none applied")
            else:
                lines.append(
                    f"Memory influence evaluated: {e.get('count', 0)} signals generated"
                )

    # ---- 2. Preference resolution (Day 29.1) ----
    for e in events:
        kind = e.get("kind")

        if kind.startswith("preference_"):
            preference_system_seen = True

        if kind == "preference_accepted":
            lines.append(
                f"Preference resolved: {e.get('key')} (weight: {e.get('weight')})"
            )
            scope = e.get("scope")
            if scope:
                lines.extend(_format_scope(scope))
            lines.append("  Result: eligible (not consumed)")

        elif kind == "preference_rejected":
            lines.append(
                f"Preference rejected: {e.get('key')} (reason: {e.get('reason')})"
            )

    # ---- 3. Preference preview & confirmation (Day 29.2) ----
    for e in events:
        kind = e.get("kind")

        if kind == "preference_preview":
            preview_seen = True
            lines.extend(_format_previews(e.get("items", [])))

        elif kind == "preference_confirmed":
            confirmation_seen = True
            keys = ", ".join(sorted(e.get("keys", []))) or "—"
            lines.append(f"Preferences confirmed: {keys}")

        elif kind == "preference_rejected_by_user":
            keys = ", ".join(sorted(e.get("keys", []))) or "—"
            lines.append(f"Preferences rejected by user: {keys}")

    if preview_seen and not confirmation_seen:
        lines.append("No preferences confirmed yet.")

    # ---- 4. Output preference consumption ----
    for e in events:
        kind = e.get("kind")

        if kind.startswith("output_preference"):
            preference_system_seen = True

        if kind == "output_preference_allowed":
            lines.append(f"Output preferences allowed ({e.get('reason')})")

        elif kind == "output_preference_blocked":
            lines.append(f"Output preferences blocked: {e.get('reason')}")

        elif kind == "output_preference_applied":
            applied_any = True
            lines.append(
                f"Output preference applied: {e.get('key')} = {e.get('value')} (surface: phrasing)"
            )

        elif kind == "output_preference_ignored":
            lines.append(
                f"Output preference ignored: {e.get('key')} ({e.get('reason')})"
            )

        elif kind == "output_preference_opt_out":
            lines.append("Output preference usage disabled by user")

        elif kind == "output_preference_reset":
            lines.append("Output preferences reset for this session")

        elif kind == "output_preference_session_expired":
            lines.append("Output preference usage expired at session end")

    # ---- 5. Explicit no-effect summary ----
    if preference_system_seen and not applied_any:
        lines.append("No output preferences affected the response.")

    return lines


# ---------- Output Preference Application ----------

def apply_output_preferences(
    text: str,
    output_prefs: Optional[OutputPreferences],
) -> str:
    """
    Output-only preference application hook.
    Deterministic. Safe no-op if unused.
    """
    if output_prefs is None or output_prefs.is_empty():
        return text

    result = text

    if output_prefs.verbosity == "short":
        result = result.split(".")[0].strip() + "."
    elif output_prefs.verbosity == "long":
        result = result  # explicit no-op

    if output_prefs.format == "bullet":
        result = "- " + result.replace(". ", "\n- ")

    return result


# ---------- Public Explain APIs ----------

def explain_last(trace_events: list) -> List[str]:
    output: List[str] = []
    output.extend(format_core_trace(trace_events))
    output.extend(format_memory_trace(trace_events))
    output.extend(format_influence_trace(trace_events))
    return output


def explain_all(trace_events: list) -> List[str]:
    output: List[str] = []
    output.extend(format_core_trace(trace_events))
    output.extend(format_memory_trace(trace_events))
    output.extend(format_influence_trace(trace_events))
    return output
