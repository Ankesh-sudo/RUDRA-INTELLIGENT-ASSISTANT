class AuthorityContract:
    """
    Declarative authority boundaries.
    Persona is NEVER allowed to perform these actions.
    """

    FORBIDDEN_CAPABILITIES = {
        "execute_actions",
        "access_memory",
        "modify_reasoning",
        "override_safety",
        "initiate_output",
    }

    @classmethod
    def is_forbidden(cls, capability: str) -> bool:
        return capability in cls.FORBIDDEN_CAPABILITIES
