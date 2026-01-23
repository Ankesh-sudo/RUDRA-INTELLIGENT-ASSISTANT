import pytest

from core.os.action_spec import ActionSpec
from core.os.control_capabilities import OSControlCapability
from core.os.executor.guarded_executor import GuardedExecutor


def test_os_control_action_is_blocked_safely():
    """
    Day 61 contract test.

    Guarantees:
    - OS_CONTROL ActionSpec can be constructed
    - GuardedExecutor routes it to stub
    - No permission / consent is triggered
    - No OS execution happens
    """

    action = ActionSpec(
        action_type="OS_CONTROL",
        target=None,
        capability=OSControlCapability.WINDOW_FOCUS,
        parameters={"app": "firefox"},
        risk_level="LOW",
        required_scopes={"OS_WINDOW_CONTROL"},
    )

    executor = GuardedExecutor()
    plan = executor.execute(action)

    # ExecutionPlan assertions
    assert plan.dry_run is True
    assert plan.action_type == "OS_CONTROL"

    # Explanation assertions
    explanation = plan.explanation
    assert explanation["status"] == "not_implemented"
    assert "OS control capability" in explanation["message"]
    assert explanation["details"]["capability"] == OSControlCapability.WINDOW_FOCUS
