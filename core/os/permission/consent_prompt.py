from core.os.permission.permission_registry import PermissionRegistry


class ConsentPrompt:
    """
    Builds consent prompt payloads.

    Responsibilities:
    - Explain *why* permission is required
    - Describe *what* action is blocked
    - NEVER grant permissions
    - NEVER interact with the user
    - Pure explanation / metadata layer
    """

    @staticmethod
    def build(action_spec, missing_scopes: set[str]) -> dict:
        """
        Canonical builder used by PermissionEvaluator.

        Args:
            action_spec: ActionSpec being evaluated
            missing_scopes: scopes not yet granted

        Returns:
            Dict payload describing the consent requirement
        """

        return {
            "action_type": action_spec.action_type,
            "category": action_spec.category,
            "target": action_spec.target,
            "required_scopes": list(missing_scopes),
            "risk_level": action_spec.risk_level,
            "reason": (
                "Permission is required to safely perform this action."
                if missing_scopes
                else "This action is high-risk and requires explicit confirmation."
            ),
        }

    # -------------------------------------------------
    # Legacy / informational helper (NON-AUTHORITATIVE)
    # -------------------------------------------------
    @staticmethod
    def build_for_action(action_type: str) -> dict:
        """
        Legacy / informational builder.

        NOT used by PermissionEvaluator.
        Safe to keep for UI previews, docs, or logs.
        """

        required_scopes = PermissionRegistry.get_required_scopes(action_type)

        return {
            "action_type": action_type,
            "required_scopes": list(required_scopes),
            "reason": "Permission required to proceed with this action.",
        }
