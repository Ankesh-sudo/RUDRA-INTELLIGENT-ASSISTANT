class UserConsentGate:

    def requires_consent(self) -> bool:
        return True

    def build_prompt(self, memory_summary: str) -> str:
        return f"Do you want me to remember that {memory_summary}?"
