class ConsentPrompt:
    """
    Builds a consent prompt payload.
    No user interaction.
    """

    @staticmethod
    def build(action_spec, missing_scopes: set) -> dict:
        return {
            "action_type": action_spec.action_type,
            "risk_level": action_spec.risk_level,
            "required_scopes": list(action_spec.required_scopes),
            "missing_scopes": list(missing_scopes),
            "reason": "Permission required to proceed with this action",
        }
