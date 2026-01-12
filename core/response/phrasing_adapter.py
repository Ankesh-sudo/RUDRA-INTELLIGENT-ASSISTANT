from typing import List, Tuple

from core.memory.influence.preference_schema import PreferenceInfluence, PreferenceType
from core.memory.influence.weighting import InfluenceWeight


class PhrasingAdapter:
    """
    Applies soft, non-authoritative phrasing adjustments
    based on preference influence.
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

            # LANGUAGE + THEME intentionally ignored for now (safe no-op)

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
            return text.split(".")[0] + "."
        return text

    @staticmethod
    def _apply_format(text: str, fmt: str) -> str:
        if fmt == "bullets":
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            return "\n".join(f"- {s}." for s in sentences)
        return text
