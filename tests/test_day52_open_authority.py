"""
Day 52 — Browser vs App Authority Tests

This test verifies:
- open youtube  → browser
- open calculator → app
- open chrome → app (browser app)
"""

import sys
import os

# 🔹 Ensure project root is on PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.orchestrator.command_orchestrator import CommandOrchestrator
from core.os.permission.permission_registry import PermissionRegistry
from core.nlp.intent import Intent


def setup():
    """
    Ensure OPEN_APP permission is granted once
    """
    PermissionRegistry.grant_action("OPEN_APP")


def test_open_youtube_browser():
    orch = CommandOrchestrator()
    result = orch.execute(Intent.OPEN_APP, {"app_name": "youtube"})

    print("\n[Test] open youtube")
    print(result)

    assert result["type"] == "action_result"
    assert result["result"]["mode"] == "browser"


def test_open_calculator_app():
    orch = CommandOrchestrator()
    result = orch.execute(Intent.OPEN_APP, {"app_name": "calculator"})

    print("\n[Test] open calculator")
    print(result)

    assert result["type"] == "action_result"
    assert result["result"]["mode"] == "app"


def test_open_chrome_app():
    orch = CommandOrchestrator()
    result = orch.execute(Intent.OPEN_APP, {"app_name": "chrome"})

    print("\n[Test] open chrome")
    print(result)

    assert result["type"] == "action_result"
    assert result["result"]["mode"] == "app"


if __name__ == "__main__":
    setup()

    test_open_youtube_browser()
    test_open_calculator_app()
    test_open_chrome_app()

    print("\n✅ Day 52 tests passed successfully.")
