from core.os.permission.scopes import (
    TERMINAL_EXEC,
    SYSTEM_INFO,
    SCREEN_CAPTURE,
    FILE_READ,
    FILE_DELETE,
    SYSTEM_CONTROL,
    NETWORK_CONTROL,
)


class PermissionRegistry:
    """
    Explicit OS permission registry.

    Design principles:
    - Scope-based (not intent-based)
    - ONLY dangerous capabilities require permission
    - App launches are SAFE by default
    - Terminal UI ≠ command execution
    - Unknown actions default to SAFE
    """

    # -------------------------------------------------
    # Action → required scopes
    # -------------------------------------------------
    _REGISTRY = {
        # -----------------------------
        # 🟢 SAFE UI / APP LAUNCH
        # -----------------------------
        # No permission required
        "OPEN_APP": set(),
        "OPEN_BROWSER": set(),
        "OPEN_YOUTUBE": set(),
        "OPEN_FILE_MANAGER": set(),
        "OPEN_TERMINAL": set(),   # 🔒 UI only, NOT execution

        # -----------------------------
        # 🟢 SAFE SYSTEM INSPECTION
        # -----------------------------
        "SYSTEM_INFO": set(),

        # -----------------------------
        # 🔴 COMMAND EXECUTION (DANGEROUS)
        # -----------------------------
        "RUN_COMMAND": {TERMINAL_EXEC},

        # -----------------------------
        # 🔴 FILE SYSTEM
        # -----------------------------
        "FILE_READ": {FILE_READ},
        "FILE_DELETE": {FILE_DELETE},

        # -----------------------------
        # 🔴 SCREEN / PRIVACY
        # -----------------------------
        "SCREEN_CAPTURE": {SCREEN_CAPTURE},

        # -----------------------------
        # 🔴 SYSTEM / NETWORK
        # -----------------------------
        "SYSTEM_CONTROL": {SYSTEM_CONTROL},
        "NETWORK_CONTROL": {NETWORK_CONTROL},
    }

    # -------------------------------------------------
    # Runtime granted scopes (session-only)
    # -------------------------------------------------
    _GRANTED = set()

    # -------------------------------------------------
    # READ
    # -------------------------------------------------
    @classmethod
    def get_required_scopes(cls, action_type: str) -> set:
        """
        Return required scopes for an action.

        Unknown actions default to SAFE (no scopes).
        This forces explicit opt-in for dangerous behavior.
        """
        return set(cls._REGISTRY.get(action_type, set()))

    @classmethod
    def is_granted(cls, scope: str) -> bool:
        return scope in cls._GRANTED

    @classmethod
    def is_action_allowed(cls, action_type: str) -> bool:
        """
        Returns True if ALL required scopes for an action
        are already granted.
        """
        required = cls.get_required_scopes(action_type)
        return all(scope in cls._GRANTED for scope in required)

    # -------------------------------------------------
    # WRITE (USED ONLY BY CONSENT FLOW)
    # -------------------------------------------------
    @classmethod
    def grant(cls, scope: str):
        cls._GRANTED.add(scope)

    @classmethod
    def grant_action(cls, action_type: str):
        """
        Grants all scopes required for an action.
        Safe actions grant nothing.
        """
        for scope in cls.get_required_scopes(action_type):
            cls._GRANTED.add(scope)
