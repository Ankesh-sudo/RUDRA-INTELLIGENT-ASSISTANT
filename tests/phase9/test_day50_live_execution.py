import types

from core.os.action_spec import ActionSpec
from core.os.executor.guarded_executor import GuardedExecutor
from core.os.permission.scopes import APP_CONTROL, SYSTEM_INFO


def _grant(executor, scope):
    executor._consent_store.grant(scope)


def test_denied_without_permission(monkeypatch):
    executor = GuardedExecutor()

    action = ActionSpec(
        action_type="OPEN_APP",
        target="firefox",
        parameters={"app_name": "firefox"},
        risk_level="LOW",
        required_scopes={APP_CONTROL},
    )

    plan = executor.execute(action)

    assert plan.dry_run is True
    assert plan.explanation["permission"] == "DENIED"


def test_confirmation_required_for_high_risk(monkeypatch):
    executor = GuardedExecutor()
    _grant(executor, SYSTEM_INFO)

    action = ActionSpec(
        action_type="DELETE_FILE",
        target="/tmp/a.txt",
        parameters={"path": "/tmp/a.txt"},
        risk_level="HIGH",
        required_scopes={SYSTEM_INFO},
    )

    plan = executor.execute(action)

    assert plan.dry_run is True
    assert plan.explanation["permission"] == "CONFIRMATION_REQUIRED"


def test_open_app_executes_when_granted(monkeypatch):
    executor = GuardedExecutor()
    _grant(executor, APP_CONTROL)

    # Mock the Linux backend call
    from core.os.linux import app_control
    monkeypatch.setattr(
        app_control.AppControl,
        "open_app",
        staticmethod(lambda name: {"ok": True, "mock": "opened"}),
    )

    action = ActionSpec(
        action_type="OPEN_APP",
        target="firefox",
        parameters={"app_name": "firefox"},
        risk_level="LOW",
        required_scopes={APP_CONTROL},
    )

    plan = executor.execute(action)

    assert plan.dry_run is False
    assert plan.explanation["permission"] == "GRANTED"
    assert plan.explanation["result"]["ok"] is True


def test_system_info_executes_when_granted(monkeypatch):
    executor = GuardedExecutor()
    _grant(executor, SYSTEM_INFO)

    from core.os.linux import system_info
    monkeypatch.setattr(
        system_info.SystemInfo,
        "uname",
        staticmethod(lambda: {"ok": True, "mock": "uname"}),
    )

    action = ActionSpec(
        action_type="SYSTEM_INFO",
        target="system",
        parameters={},
        risk_level="LOW",
        required_scopes={SYSTEM_INFO},
    )

    plan = executor.execute(action)

    assert plan.dry_run is False
    assert plan.explanation["permission"] == "GRANTED"
    assert plan.explanation["result"]["ok"] is True


def test_non_whitelisted_action_never_executes(monkeypatch):
    executor = GuardedExecutor()
    _grant(executor, APP_CONTROL)

    action = ActionSpec(
        action_type="UNSUPPORTED_ACTION",
        target="x",
        parameters={},
        risk_level="LOW",
        required_scopes=set(),
    )

    plan = executor.execute(action)

    assert plan.dry_run is False
    assert plan.explanation["permission"] == "GRANTED"
    assert plan.explanation["result"]["ok"] is False
