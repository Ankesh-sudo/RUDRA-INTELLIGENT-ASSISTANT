"""
MASTER TEST — DAY 17
Covers:
- Day 15: confidence gating
- Day 16: global intent threshold
- Day 17.1–17.5: clarification + follow-ups
- Day 17.6: slot detection & recovery
"""

import pytest

from core.actions.action_executor import ActionExecutor
from core.nlp.intent import Intent
from core.context.short_term import ShortTermContext


# ===============================
# FIXTURE
# ===============================
@pytest.fixture
def executor():
    return ActionExecutor()


# ===============================
# DAY 15 — CONFIDENCE GATING
# ===============================
def test_low_confidence_blocked(executor):
    result = executor.execute(
        Intent.OPEN_BROWSER,
        "open browser",
        confidence=0.1,
    )
    assert result["success"] is False
    assert result["executed"] is False


def test_dangerous_intent_requires_high_confidence(executor):
    result = executor.execute(
        Intent.OPEN_TERMINAL,
        "open terminal",
        confidence=0.5,
    )
    assert result["success"] is False


# ===============================
# DAY 16 — GLOBAL CONFIDENCE
# ===============================
def test_unknown_intent_rejected(executor):
    result = executor.execute(
        Intent.UNKNOWN,
        "blah blah",
        confidence=0.9,
    )
    assert result["executed"] is False


# ===============================
# DAY 17.1 — CLARIFICATION SAFE
# ===============================
def test_clarification_does_not_execute(executor):
    result = executor.execute(
        Intent.SEARCH_WEB,
        "search",
        confidence=0.9,
    )
    assert result["success"] is False
    assert "query" in result["message"].lower()


# ===============================
# DAY 17.4 — PRONOUN BLOCK
# ===============================
def test_pronoun_without_context_blocked(executor):
    result = executor.execute(
        Intent.OPEN_BROWSER,
        "open it",
        confidence=0.9,
    )
    assert result["executed"] is False


# ===============================
# DAY 17.5 — FOLLOW-UP RECOVERY
# ===============================
def test_followup_repeat_allowed(executor):
    # initial action
    r1 = executor.execute(
        Intent.OPEN_BROWSER,
        "open github",
        confidence=1.0,
    )
    assert r1["success"] is True

    # follow-up repeat
    r2 = executor.execute(
        Intent.OPEN_BROWSER,
        "open it again",
        confidence=0.9,
    )
    assert r2["success"] is True
    assert r2.get("is_followup") is True


# ===============================
# DAY 17.6 — SLOT DETECTION
# ===============================
def test_slot_missing_detected(executor):
    missing = executor.get_missing_args(
        Intent.SEARCH_WEB,
        "search"
    )
    assert missing == ["query"]


def test_slot_not_missing_when_present(executor):
    missing = executor.get_missing_args(
        Intent.SEARCH_WEB,
        "search python decorators"
    )
    assert missing == []


# ===============================
# DAY 17.6 — SLOT RECOVERY
# ===============================
def test_single_slot_recovery_uses_full_text(executor):
    recovered = executor.fill_missing(
        Intent.SEARCH_WEB,
        followup_text="python decorators",
        missing=["query"],
    )
    assert recovered["query"] == "python decorators"


def test_slot_recovery_executes_successfully(executor):
    # simulate recovered execution
    result = executor.execute(
        Intent.SEARCH_WEB,
        text="search",
        confidence=0.85,
        replay_args={"query": "python decorators"},
    )
    assert result["success"] is True


# ===============================
# REGRESSION — CONTEXT SAFETY
# ===============================
def test_context_not_leaked_between_intents(executor):
    r1 = executor.execute(
        Intent.OPEN_BROWSER,
        "open github",
        confidence=1.0,
    )
    assert r1["success"]

    r2 = executor.execute(
        Intent.SEARCH_WEB,
        "search it",
        confidence=0.9,
    )
    assert r2["success"] is False


# ===============================
# FINAL GUARANTEE
# ===============================
def test_action_history_capped(executor):
    for _ in range(30):
        executor.execute(
            Intent.OPEN_BROWSER,
            "open google",
            confidence=1.0,
        )
    assert len(executor.action_history) <= 20
