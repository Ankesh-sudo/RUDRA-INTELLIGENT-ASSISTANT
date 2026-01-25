from core.dialogue.dialogue_turn import DialogueTurn, Speaker
from core.dialogue.dialogue_types import DialogueIntent


class DialogueEngine:
    """
    Dialogue layer (Day 70)

    Guarantees:
    - No actions
    - No memory writes
    - No TTS
    - No persona access
    - Deterministic resolution only
    """

    def resolve(self, text: str, context: dict) -> DialogueTurn:
        intent = self._extract_intent(text)
        response_plan = self._plan_response(intent)

        return DialogueTurn(
            speaker=Speaker.ASSISTANT,
            intent=intent,
            context_snapshot=context,
            response_plan=response_plan,
        )

    # -------------------------------
    # Internal helpers (pure functions)
    # -------------------------------

    def _extract_intent(self, text: str) -> DialogueIntent:
        """
        Meaning extraction only.
        No guessing, no ML, no side effects.
        """
        normalized = text.lower().strip()

        if "how are you" in normalized:
            return DialogueIntent.EMOTIONAL_CHECK

        if normalized in {"ok", "okay", "thanks", "thank you"}:
            return DialogueIntent.ACKNOWLEDGEMENT

        if normalized.endswith("?"):
            return DialogueIntent.CLARIFICATION

        return DialogueIntent.SMALL_TALK

    def _plan_response(self, intent: DialogueIntent) -> str:
        """
        Plans WHAT to say, not HOW to say it.
        No tone, no persona, no voice decisions.
        """
        if intent == DialogueIntent.EMOTIONAL_CHECK:
            return "Acknowledge politely without emotional dependency."

        if intent == DialogueIntent.ACKNOWLEDGEMENT:
            return "Respond briefly and neutrally."

        if intent == DialogueIntent.CLARIFICATION:
            return "Provide a short, clear clarification."

        if intent == DialogueIntent.SMALL_TALK:
            return "Maintain neutral conversational flow."

        return "Respond safely and minimally."
