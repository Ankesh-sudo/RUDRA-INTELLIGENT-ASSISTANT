from dataclasses import dataclass
from typing import Dict, Any, FrozenSet

from core.os.permission.scopes import (
    ALL_SCOPES,
    SYSTEM_INFO,
    GUI_APP_LAUNCH,
)

# ==========================================================
# CONSTANTS (SEALED)
# ==========================================================

_ALLOWED_RISK_LEVELS = {"LOW", "MEDIUM", "HIGH"}
_ALLOWED_ACTION_CATEGORIES = {"SYSTEM", "APP", "FILE"}

_ACTION_CATEGORY_MAP = {
    "OPEN_APP": "APP",
    "CLOSE_APP": "APP",
    "SYSTEM_INFO": "SYSTEM",
    "FILE_DELETE": "FILE",
    "FILE_READ": "FILE",
}

# Legacy / backward-compat fields (IGNORED)
_LEGACY_FIELDS = {
    "category",
    "destructive",
    "supports_undo",
    "requires_preview",
}


# ==========================================================
# ACTION SPEC — PHASE 9 + DAY 55 (LOCKED)
# ==========================================================

@dataclass(frozen=True, init=False)
class ActionSpec:
    """
    Immutable, declarative description of an executable action.

    Guarantees:
    - Registry agnostic
    - Execution agnostic
    - Backward compatible (Day-55)
    """

    action_type: str
    category: str
    target: str | None
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
        } | _LEGACY_FIELDS

        unknown = set(kwargs.keys()) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields: {unknown}")

        try:
            action_type = kwargs["action_type"]
            target = kwargs.get("target")
            parameters = kwargs.get("parameters", {})
            risk_level = kwargs["risk_level"]
            required_scopes = kwargs["required_scopes"]
        except KeyError as e:
            raise ValueError(f"Missing required field: {e.args[0]}")

        # --------------------------------------------------
        # BASIC VALIDATION (STRUCTURAL)
        # --------------------------------------------------

        if not isinstance(action_type, str) or not action_type.strip():
            raise ValueError("action_type must be non-empty string")

        if target is not None and not isinstance(target, str):
            raise ValueError("target must be string or None")

        if not isinstance(parameters, dict):
            raise ValueError("parameters must be dict")

        if risk_level not in _ALLOWED_RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {risk_level}")

        if not isinstance(required_scopes, (set, frozenset)):
            raise ValueError("required_scopes must be set or frozenset")

        # --------------------------------------------------
        # PERMISSION SCOPE VALIDATION
        # --------------------------------------------------

        SAFE_SCOPES = {SYSTEM_INFO, GUI_APP_LAUNCH, "open_app"}

        for scope in required_scopes:
            if not isinstance(scope, str):
                raise ValueError(f"Invalid permission scope: {scope}")

            if scope not in ALL_SCOPES and scope not in SAFE_SCOPES:
                raise ValueError(f"Invalid permission scope: {scope}")

        # --------------------------------------------------
        # DERIVED FIELDS
        # --------------------------------------------------

        category = _ACTION_CATEGORY_MAP.get(action_type, "SYSTEM")
        if category not in _ALLOWED_ACTION_CATEGORIES:
            raise ValueError(f"Invalid derived category: {category}")

        requires_confirmation = risk_level == "HIGH"

        # --------------------------------------------------
        # FREEZE (IMMUTABLE)
        # --------------------------------------------------

        object.__setattr__(self, "action_type", action_type)
        object.__setattr__(self, "category", category)
        object.__setattr__(self, "target", target)
        object.__setattr__(self, "parameters", parameters)
        object.__setattr__(self, "risk_level", risk_level)
        object.__setattr__(
            self, "required_scopes", frozenset(required_scopes)
        )
        object.__setattr__(
            self, "requires_confirmation", requires_confirmation
        )
    @property
    def destructive(self) -> bool:
        return bool(self.requires_confirmation)
