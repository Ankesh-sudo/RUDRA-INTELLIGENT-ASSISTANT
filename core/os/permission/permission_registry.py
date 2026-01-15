class PermissionRegistry:
    """
    Day 50 – Explicit OS permission registry

    - Scope-based (not action-spec based)
    - Stateless except for granted scopes
    - Single source of truth for permissions
    """

    # Action → required scopes
    _REGISTRY = {
        # App control (Chrome, Firefox, Calculator, etc.)
        "OPEN_APP": {"APP_CONTROL"},

        # System inspection
        "SYSTEM_INFO": {"SYSTEM_INFO"},
    }

    # Granted scopes (runtime)
    _GRANTED = set()

    # -------------------------------------------------
    # READ
    # -------------------------------------------------
    @classmethod
    def get_required_scopes(cls, action_type: str) -> set:
        return cls._REGISTRY.get(action_type, set())

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
    # WRITE
    # -------------------------------------------------
    @classmethod
    def grant(cls, scope: str):
        cls._GRANTED.add(scope)

    @classmethod
    def grant_action(cls, action_type: str):
        """
        Grants all scopes required for an action.
        """
        for scope in cls.get_required_scopes(action_type):
            cls._GRANTED.add(scope)
