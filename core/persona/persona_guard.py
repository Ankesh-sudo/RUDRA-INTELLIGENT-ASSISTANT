import re
from typing import List


class PersonaGuard:
    """
    Enforces meaning-preservation invariants.
    Conservative by design: better to reject than alter.

    Day 31.3 additions:
    - Prefix preservation check (for suffix-only expressiveness)
    """

    @staticmethod
    def _normalize(text: str) -> List[str]:
        """
        Normalize text for strict semantic comparison.
        """
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text.split()

    @classmethod
    def is_semantically_safe(cls, original: str, transformed: str) -> bool:
        """
        Semantic safety rule (Day 31.2, unchanged):

        - Same word sequence
        - Same length
        - Same order

        Note:
        This is NOT used to validate suffix expressiveness.
        It validates the semantic core only.
        """
        if original == transformed:
            return True

        o = cls._normalize(original)
        t = cls._normalize(transformed)

        if len(o) != len(t):
            return False

        return o == t

    @classmethod
    def is_prefix_preserved(cls, original: str, transformed: str) -> bool:
        """
        Day 31.3 rule:

        Persona output MUST preserve original text as a prefix.
        This allows suffix-only expressiveness (emoji / warmth)
        while forbidding rewording, insertion, or deletion.
        """
        return transformed.startswith(original)
