# tests/phase9/test_day47_action_spec.py

import pytest

from core.os.action_spec import ActionSpec
from core.os.permission.scopes import APP_CONTROL, SYSTEM_INFO


def test_valid_action_spec_passes():
    spec = ActionSpec(
        action_type="OPEN_APP",
        target="firefox",
        parameters={"app_name": "firefox"},
        risk_level="LOW",
        required_scopes={APP_CONTROL},
    )
    assert spec.action_type == "OPEN_APP"
    assert spec.risk_level == "LOW"
    assert APP_CONTROL in spec.required_scopes


def test_missing_required_field_fails():
    with pytest.raises(ValueError):
        ActionSpec(
            action_type="OPEN_APP",
            target="firefox",
            parameters={"app_name": "firefox"},
            # risk_level missing
            required_scopes={APP_CONTROL},
        )


def test_unknown_field_fails():
    with pytest.raises(ValueError):
        ActionSpec(
            action_type="OPEN_APP",
            target="firefox",
            parameters={"app_name": "firefox"},
            risk_level="LOW",
            required_scopes={APP_CONTROL},
            unexpected_field=True,  # not allowed
        )


def test_invalid_scope_rejected():
    with pytest.raises(ValueError):
        ActionSpec(
            action_type="OPEN_APP",
            target="firefox",
            parameters={"app_name": "firefox"},
            risk_level="LOW",
            required_scopes={"NOT_A_REAL_SCOPE"},
        )


def test_high_risk_action_requires_confirmation():
    spec = ActionSpec(
        action_type="DELETE_FILE",
        target="/tmp/test.txt",
        parameters={"path": "/tmp/test.txt"},
        risk_level="HIGH",
        required_scopes={SYSTEM_INFO},
    )
    assert spec.risk_level == "HIGH"
    assert spec.requires_confirmation is True


def test_action_spec_is_immutable():
    spec = ActionSpec(
        action_type="OPEN_APP",
        target="firefox",
        parameters={"app_name": "firefox"},
        risk_level="LOW",
        required_scopes={APP_CONTROL},
    )
    with pytest.raises(AttributeError):
        spec.action_type = "CLOSE_APP"
