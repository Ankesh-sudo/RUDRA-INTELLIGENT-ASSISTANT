"""
Slot & Preference Merger

Safely merges memory-based defaults into slots.
"""

class SlotPreferenceMerger:
    def merge(
        self,
        *,
        slots: dict,
        preferences: list[dict],
        allowed_keys: set[str]
    ) -> dict:
        """
        Merge preferences into slots without overriding user input.

        Parameters:
        - slots: extracted slots from current utterance
        - preferences: LTM preferences (list of dicts)
        - allowed_keys: which slot keys can be defaulted

        Returns:
        - merged slots
        """
        merged = dict(slots)

        for pref in preferences:
            key = pref.get("key")
            value = pref.get("value")

            if key in allowed_keys and key not in merged:
                merged[key] = value

        return merged
