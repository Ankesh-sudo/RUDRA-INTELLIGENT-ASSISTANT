from dataclasses import dataclass
from typing import Dict, Any, FrozenSet

from core.os.permission.permission_registry import PermissionRegistry
from core.os.permission.scopes import ALL_SCOPES


# ==========================================================
# CONSTANTS (SEALED)
# ==========================================================

_ALLOWED_RISK_LEVELS = {"LOW", "MEDIUM", "HIGH"}

# ⚠️ CASE-SENSITIVE — DO NOT CHANGE
_ALLOWED_ACTION_CATEGORIES = {"SYSTEM", "APP", "FILE"}


# ==========================================================
# ACTION SPEC
# ==========================================================

@dataclass(frozen=True, init=False)
class ActionSpec:
    """
    Immutable, declarative description of an executable action.

    RULES:
    - No execution logic
    - No side effects
    - No mutation
    - Strict validation
    """

    # Identity
    action_type: str
    category: str
    target: str

    # Parameters
    parameters: Dict[str, Any]

    # Safety & permission
    risk_level: str
    required_scopes: FrozenSet[str]
    requires_confirmation: bool

    # File / destructive safety
    destructive: bool
    supports_undo: bool
    requires_preview: bool

    # ------------------------------------------------------
    # CONSTRUCTOR (STRICT)
    # ------------------------------------------------------
    def __init__(self, **kwargs):
        allowed_fields = {
            "action_type",
            "category",
            "target",
            "parameters",
            "risk_level",
            "required_scopes",
            "destructive",
            "supports_undo",
            "requires_preview",
        }

        unknown = set(kwargs.keys()) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields: {unknown}")

        try:
            action_type = kwargs["action_type"]
            category = kwargs["category"]
            target = kwargs["target"]
            parameters = kwargs["parameters"]
            risk_level = kwargs["risk_level"]
            required_scopes = kwargs["required_scopes"]
            destructive = kwargs["destructive"]
            supports_undo = kwargs["supports_undo"]
            requires_preview = kwargs["requires_preview"]
        except KeyError as e:
            raise ValueError(f"Missing required field: {e.args[0]}")

        # --------------------------------------------------
        # BASIC VALIDATION
        # --------------------------------------------------


        if category not in _ALLOWED_ACTION_CATEGORIES:
            raise ValueError(f"Invalid category: {category}")


        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dict")

        if risk_level not in _ALLOWED_RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {risk_level}")

        if not isinstance(required_scopes, (set, frozenset)):
            raise ValueError("required_scopes must be a set or frozenset")

        unknown_scopes = set(required_scopes) - ALL_SCOPES
        if unknown_scopes:
            raise ValueError(f"Unknown permission scopes: {unknown_scopes}")

        if not isinstance(destructive, bool):
            raise ValueError("destructive must be boolean")

        if not isinstance(supports_undo, bool):
            raise ValueError("supports_undo must be boolean")

        if not isinstance(requires_preview, bool):
            raise ValueError("requires_preview must be boolean")

        # --------------------------------------------------
        # SAFETY INVARIANTS (NON-NEGOTIABLE)
        # --------------------------------------------------

        # Destructive actions MUST be high risk
        if destructive and risk_level != "HIGH":
            raise ValueError(
                "Destructive actions must have risk_level='HIGH'"
            )

        # All file actions MUST require preview
        if category == "FILE" and not requires_preview:
            raise ValueError(
                "File actions must require preview (requires_preview=True)"
            )

        # --------------------------------------------------
        # PERMISSION REGISTRY CONSISTENCY
        # --------------------------------------------------

        expected_scopes = PermissionRegistry.get_required_scopes(action_type)
        if expected_scopes != set(required_scopes):
            raise ValueError(
                f"Scopes mismatch for action '{action_type}'. "
                f"Expected {expected_scopes}, got {set(required_scopes)}"
            )

        # --------------------------------------------------
        # FREEZE (IMMUTABLE)
        # --------------------------------------------------

        # --------------------------------------------------
        # PERMISSION REGISTRY CONSISTENCY
        # --------------------------------------------------
        # 🔒 DAY-49 RULE:
        # High-risk actions are validated AFTER confirmation,
        # so registry scope matching is skipped here.
        if risk_level != "HIGH":
            expected = PermissionRegistry.get_required_scopes(action_type)
            if expected != set(required_scopes):
                raise ValueError(
                    f"Scopes mismatch for action '{action_type}'. "
                    f"Expected {expected}, got {set(required_scopes)}"
                )

        # --------------------------------------------------
        # FREEZE (IMMUTABLE)
        # --------------------------------------------------


        object.__setattr__(self, "action_type", action_type)
        object.__setattr__(self, "category", category)
        object.__setattr__(self, "target", target)
        object.__setattr__(self, "parameters", parameters)
        object.__setattr__(self, "risk_level", risk_level)
        object.__setattr__(self, "required_scopes", frozenset(required_scopes))
        object.__setattr__(
            self,
            "requires_confirmation",
            risk_level == "HIGH",
        )
        object.__setattr__(self, "destructive", destructive)
        object.__setattr__(self, "supports_undo", supports_undo)
        object.__setattr__(self, "requires_preview", requires_preview)
