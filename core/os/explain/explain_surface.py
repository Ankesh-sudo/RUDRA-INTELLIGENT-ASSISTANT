class ExplainSurface:
    @staticmethod
    def explain(action_spec):
        return {
            "what": f"Action '{action_spec.action_type}' will be prepared",
            "target": action_spec.target,
            "why": "Requested by user intent",
            "risk_level": action_spec.risk_level,
            "required_scopes": list(action_spec.required_scopes),
        }
