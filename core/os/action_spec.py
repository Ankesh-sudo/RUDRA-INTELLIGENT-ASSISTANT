from dataclasses import dataclass, field
from typing import Dict, Any, FrozenSet

from core.os.permission.permission_registry import PermissionRegistry
from core.os.permission.scopes import ALL_SCOPES


_ALLOWED_RISK_LEVELS = {"LOW", "MEDIUM", "HIGH"}


@dataclass(frozen=True, init=False)
class ActionSpec:
    action_type: str
    target: str
    parameters: Dict[str, Any]
    risk_level: str
    required_scopes: FrozenSet[str]
    requires_confirmation: bool

    def __init__(self, **kwargs):
        allowed_fields = {
            "action_type",
            "target",
            "parameters",
            "risk_level",
            "required_scopes",
        }

        unknown = set(kwargs.keys()) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields: {unknown}")

        try:
            action_type = kwargs["action_type"]
            target = kwargs["target"]
            parameters = kwargs["parameters"]
            risk_level = kwargs["risk_level"]
            required_scopes = kwargs["required_scopes"]
        except KeyError as e:
            raise ValueError(f"Missing required field: {e.args[0]}")

        # ---- basic validation ----
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dict")

        if risk_level not in _ALLOWED_RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {risk_level}")

        if not isinstance(required_scopes, (set, frozenset)):
            raise ValueError("required_scopes must be a set")

        unknown_scopes = set(required_scopes) - ALL_SCOPES
        if unknown_scopes:
            raise ValueError(f"Unknown permission scopes: {unknown_scopes}")

        # ---- registry consistency ----
        expected = PermissionRegistry.get_required_scopes(action_type)
        if expected != set(required_scopes):
            raise ValueError(
                f"Scopes mismatch for action '{action_type}'. "
                f"Expected {expected}, got {set(required_scopes)}"
            )

        # ---- freeze ----
        object.__setattr__(self, "action_type", action_type)
        object.__setattr__(self, "target", target)
        object.__setattr__(self, "parameters", parameters)
        object.__setattr__(self, "risk_level", risk_level)
        object.__setattr__(self, "required_scopes", frozenset(required_scopes))
        object.__setattr__(
            self,
            "requires_confirmation",
            risk_level == "HIGH",
        )
