from core.explain.explain_surface import ExplainSurface
from core.os.action_spec import ActionSpec


class OSControlStubExecutor:
    """
    Stub executor for OS control actions (Day 61).

    Guarantees:
    - No OS calls
    - No permissions
    - No consent checks
    - Always NOT_IMPLEMENTED
    """

    @staticmethod
    def execute(action_spec: ActionSpec) -> ExplainSurface:
        return ExplainSurface(
            {
                "status": "NOT_IMPLEMENTED",
                "title": "OS control not enabled",
                "message": (
                    f"OS control capability '{action_spec.capability}' "
                    "is declared but not executable yet."
                ),
                "details": {
                    "action_type": action_spec.action_type,
                    "capability": str(action_spec.capability),
                    "parameters": action_spec.parameters or {},
                },
            }
        )
