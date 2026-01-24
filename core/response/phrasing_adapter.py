from typing import List, Tuple, Optional

from core.memory.influence.preference_schema import PreferenceInfluence, PreferenceType
from core.memory.influence.weighting import InfluenceWeight
from core.response.final_envelope import FinalResponseEnvelope


class PhrasingAdapter:
    """
    Applies soft, non-authoritative phrasing adjustments
    based on preference influence.

    ⚠ This adapter does NOT implement persona behavior.
    """

    @staticmethod
    def adapt(
        text: str,
        influences: List[PreferenceInfluence],
        weight: InfluenceWeight | None = None,
    ) -> Tuple[str, List[str]]:
        """
        Returns adapted_text, explanations
        """
        adapted = text
        explanations: List[str] = []

        for influence in influences:
            if not influence.is_active():
                continue

            if influence.pref_type == PreferenceType.TONE:
                adapted = PhrasingAdapter._apply_tone(adapted, influence.value)
                explanations.append(influence.explain())

            elif influence.pref_type == PreferenceType.VERBOSITY:
                adapted = PhrasingAdapter._apply_verbosity(adapted, influence.value)
                explanations.append(influence.explain())

            elif influence.pref_type == PreferenceType.FORMAT:
                adapted = PhrasingAdapter._apply_format(adapted, influence.value)
                explanations.append(influence.explain())

            # LANGUAGE + THEME intentionally ignored (safe no-op)

        if weight:
            explanations.append(weight.explain())

        return adapted, explanations

    @staticmethod
    def _apply_tone(text: str, tone: str) -> str:
        if tone == "formal":
            return (
                text
                .replace("You", "the user")
                .replace("you", "the user")
            )
        return text

    @staticmethod
    def _apply_verbosity(text: str, verbosity: str) -> str:
        if verbosity == "low":
            return text.split(".")[0].strip() + "."
        return text

    @staticmethod
    def _apply_format(text: str, fmt: str) -> str:
        if fmt == "bullets":
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            return "\n".join(f"- {s}." for s in sentences)
        return text


# -------------------------------------------------------------------
# DAY 65–66 — MAAHI TEXT LAYER (PRESENTATION ONLY)
# -------------------------------------------------------------------

class MaahiTextAdapter:
    """
    Text-only persona phrasing adapter.

    HARD RULES:
    - NO logic
    - NO memory
    - NO permissions
    - NO OS awareness
    - NO meaning change
    """

    _PHRASE_MAP = {
        # Polished confirmations
        "CONFIRM_ACTION": "Got it, Boss. Doing it now.",

        # Polished success
        "ACTION_COMPLETE": "All set, Boss.",

        # Polished failure (no explanation added)
        "ACTION_FAILED": "Sorry Boss, that didn’t work.",

        # Polished confirmation request
        "WAITING_CONFIRM": "Boss, should I go ahead?",

        # Polished cancellation
        "CANCELLED": "Okay Boss, I’ve cancelled it.",
    }

    @staticmethod
    def apply(envelope: FinalResponseEnvelope) -> str:
        """
        Returns final user-visible text.

        Canonical text remains envelope.final_text.
        """
        # Persona not applied → passthrough
        if not envelope.persona_applied:
            return envelope.final_text

        # No hint → passthrough
        if not envelope.persona_hint:
            return envelope.final_text

        # Deterministic lookup only
        phrased = MaahiTextAdapter._PHRASE_MAP.get(
            envelope.persona_hint
        )

        # Unknown hint → passthrough
        if not phrased:
            return envelope.final_text

        return phrased
