import re
from typing import List


class PersonaGuard:
    """
    Enforces meaning-preservation invariants.
    Conservative by design: better to reject than alter.
    """

    @staticmethod
    def _normalize(text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text.split()

    @classmethod
    def is_semantically_safe(cls, original: str, transformed: str) -> bool:
        """
        Hard rule (Day 31.2):
        - Same word multiset
        - Same length
        - Same order (for now)
        """
        if original == transformed:
            return True

        o = cls._normalize(original)
        t = cls._normalize(transformed)

        if len(o) != len(t):
            return False

        return o == t
