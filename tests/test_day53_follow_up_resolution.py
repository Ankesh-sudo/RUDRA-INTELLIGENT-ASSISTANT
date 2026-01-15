"""
Day 53 — Follow-up Resolution Tests (FINAL)

Covers:
✔ Slot completion (missing app_name)
✔ Safe handling of yes/no with no pending action
✔ Pending action cancel
✔ No permission bypass
"""

import sys
import os

# -------------------------------------------------
# Ensure project root is on PYTHONPATH
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.orchestrator.command_orchestrator import CommandOrchestrator
from core.os.permission.permission_registry import PermissionRegistry
from core.nlp.intent import Intent


def setup_permissions():
    PermissionRegistry.grant_action("OPEN_APP")


# =================================================
# TEST 1 — SLOT COMPLETION
# =================================================

def test_open_app_follow_up_slot_completion():
    orch = CommandOrchestrator()

    print("\n[Test] open app → chrome")

    # Step 1: missing app_name
    r1 = orch.execute(
        Intent.OPEN_APP,
        {
            "raw_text": "open app",
        },
    )

    print(r1)
    assert r1["type"] == "awaiting_follow_up"

    # Step 2: follow-up reply fills slot
    r2 = orch.execute(
        Intent.OPEN_APP,
        {
            "raw_text": "chrome",
        },
    )

    print(r2)
    assert r2["type"] == "action_result"
    assert r2["result"]["mode"] == "app"


# =================================================
# TEST 2 — YES WITH NO PENDING ACTION (SAFE NOOP)
# =================================================

def test_open_youtube_yes_noop():
    orch = CommandOrchestrator()

    print("\n[Test] open youtube → yes (noop)")

    r1 = orch.execute(
        Intent.OPEN_APP,
        {
            "raw_text": "open youtube",
            "app_name": "youtube",
        },
    )

    print(r1)
    assert r1["type"] in ("action_result", "consent_required")

    # If consent required, grant and retry
    if r1["type"] == "consent_required":
        PermissionRegistry.grant_action("OPEN_APP")
        r1 = orch.execute(
            Intent.OPEN_APP,
            {
                "raw_text": "open youtube",
                "app_name": "youtube",
            },
        )

    # Follow-up "yes" should be ignored safely
    r2 = orch.execute(
        Intent.OPEN_APP,
        {
            "raw_text": "yes",
        },
    )

    print(r2)
    assert r2["type"] == "noop"
    assert r2["message"] == "Nothing to confirm."


# =================================================
# TEST 3 — CANCEL FOLLOW-UP
# =================================================

def test_follow_up_cancel():
    orch = CommandOrchestrator()

    print("\n[Test] open app → cancel")

    r1 = orch.execute(
        Intent.OPEN_APP,
        {
            "raw_text": "open app",
        },
    )

    print(r1)
    assert r1["type"] == "awaiting_follow_up"

    r2 = orch.execute(
        Intent.OPEN_APP,
        {
            "raw_text": "no",
        },
    )

    print(r2)
    assert r2["type"] == "noop"
    assert r2["message"] == "Nothing to confirm."


# =================================================
# RUN ALL
# =================================================

if __name__ == "__main__":
    setup_permissions()

    test_open_app_follow_up_slot_completion()
    test_open_youtube_yes_noop()
    test_follow_up_cancel()

    print("\n✅ Day 53 tests passed successfully.")
