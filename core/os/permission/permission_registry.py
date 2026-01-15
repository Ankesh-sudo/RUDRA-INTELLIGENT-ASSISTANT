class PermissionRegistry:
    """
    Day 50 – Explicit OS permission registry
    """

    _REGISTRY = {
        # App control (Chrome, Firefox, Calculator, etc.)
        "OPEN_APP": {"APP_CONTROL"},

        # System inspection
        "SYSTEM_INFO": {"SYSTEM_INFO"},
    }

    _GRANTED = set()

    @classmethod
    def get_required_scopes(cls, action_type: str) -> set:
        return cls._REGISTRY.get(action_type, set())

    @classmethod
    def grant(cls, scope: str):
        cls._GRANTED.add(scope)

    @classmethod
    def is_granted(cls, scope: str) -> bool:
        return scope in cls._GRANTED
