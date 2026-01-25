from .persona_mode import PersonaMode
from .persona_policy import PersonaPolicy
from .persona_guardrails import GuardrailResult


class PersonaExplain:
    """
    Explainability surface for persona maturity.
    """

    @staticmethod
    def explain(
        *,
        mode: PersonaMode,
        guardrail_result: GuardrailResult,
    ) -> dict:
        return {
            "mode": mode.value,
            "limits": {
                "max_sentence_length": PersonaPolicy.MAX_SENTENCE_LENGTH,
                "max_affection_markers": PersonaPolicy.MAX_AFFECTION_MARKERS,
                "forbidden_phrases": sorted(PersonaPolicy.FORBIDDEN_PHRASES),
            },
            "approved": guardrail_result.approved,
            "reason": guardrail_result.reason,
        }
