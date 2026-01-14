class PermissionRegistry:
    _REGISTRY = {
        "OPEN_APP": {"APP_CONTROL"},
        "DELETE_FILE": {"SYSTEM_INFO"},
    }

    @classmethod
    def get_required_scopes(cls, action_type: str) -> set:
        return cls._REGISTRY.get(action_type, set())
