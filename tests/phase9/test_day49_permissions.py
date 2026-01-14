from core.os.action_spec import ActionSpec
from core.os.executor.guarded_executor import GuardedExecutor
from core.os.permission.scopes import APP_CONTROL, SYSTEM_INFO


def _open_app_action():
    return ActionSpec(
        action_type="OPEN_APP",
        target="firefox",
        parameters={"app_name": "firefox"},
        risk_level="LOW",
        required_scopes={APP_CONTROL},
    )


def test_action_denied_when_scope_missing():
    executor = GuardedExecutor()

    plan = executor.execute(_open_app_action())

    assert plan.explanation["permission"] == "DENIED"
    assert "prompt" in plan.explanation


def test_action_allowed_when_scope_granted():
    executor = GuardedExecutor()
    executor._consent_store.grant(APP_CONTROL)

    plan = executor.execute(_open_app_action())

    assert plan.explanation["permission"] == "GRANTED"


def test_high_risk_action_requires_confirmation():
    action = ActionSpec(
        action_type="DELETE_FILE",
        target="/tmp/a.txt",
        parameters={"path": "/tmp/a.txt"},
        risk_level="HIGH",
        required_scopes={SYSTEM_INFO},
    )

    executor = GuardedExecutor()
    executor._consent_store.grant(SYSTEM_INFO)

    plan = executor.execute(action)

    assert plan.explanation["permission"] == "CONFIRMATION_REQUIRED"
    assert "prompt" in plan.explanation


def test_prompt_payload_present_when_needed():
    executor = GuardedExecutor()

    plan = executor.execute(_open_app_action())

    assert "prompt" in plan.explanation
    assert plan.explanation["prompt"]["action_type"] == "OPEN_APP"


def test_persona_cannot_affect_permission():
    executor = GuardedExecutor()

    plan = executor.execute(_open_app_action())

    explanation_text = str(plan.explanation).lower()
    assert "persona" not in explanation_text
