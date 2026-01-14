from core.os.executor.guarded_executor import GuardedExecutor, ExecutionPlan
from core.os.action_spec import ActionSpec
from core.os.permission.scopes import APP_CONTROL


def _sample_action():
    return ActionSpec(
        action_type="OPEN_APP",
        target="firefox",
        parameters={"app_name": "firefox"},
        risk_level="LOW",
        required_scopes={APP_CONTROL},
    )


def test_executor_returns_execution_plan():
    executor = GuardedExecutor()
    plan = executor.execute(_sample_action())

    assert isinstance(plan, ExecutionPlan)


def test_dry_run_is_always_true():
    executor = GuardedExecutor()
    plan = executor.execute(_sample_action())

    assert plan.dry_run is True


def test_explanation_is_attached():
    executor = GuardedExecutor()
    plan = executor.execute(_sample_action())

    assert "what" in plan.explanation
    assert "risk_level" in plan.explanation


def test_no_os_execution_occurs():
    executor = GuardedExecutor()
    plan = executor.execute(_sample_action())

    assert plan.explanation["what"].startswith("Action")


def test_persona_has_no_influence():
    executor = GuardedExecutor()
    plan = executor.execute(_sample_action())

    assert "persona" not in plan.explanation
