from core.os.permission.permission_registry import PermissionRegistry


class ConsentPrompt:
    """
    Builds a consent prompt payload.
    No user interaction.
    No permission granting.
    Pure explanation layer.
    """

    @staticmethod
    def build_for_action(action_type: str) -> dict:
        """
        Returns a consent payload describing
        why permission is required for this action.
        """

        required_scopes = PermissionRegistry.get_required_scopes(action_type)

        return {
            "action_type": action_type,
            "required_scopes": list(required_scopes),
            "reason": "Permission required to proceed with this action",
        }
