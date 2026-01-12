# core/memory/deduplicator.py

import re


class MemoryDeduplicator:
    PREFERENCE_VERBS = [
        "like", "love", "prefer", "enjoy", "dislike", "hate"
    ]

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _remove_preference_verbs(self, text: str) -> str:
        for verb in self.PREFERENCE_VERBS:
            text = re.sub(rf"\b{verb}\b", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def check(self, new_entry, existing_entries) -> str:
        new_norm = self._normalize(new_entry.content)

        for entry in existing_entries:
            if entry.type != new_entry.type:
                continue

            existing_norm = self._normalize(entry.content)

            # Exact duplicate
            if existing_norm == new_norm:
                return "duplicate"

            # Near duplicate (same core meaning)
            new_core = self._remove_preference_verbs(new_norm)
            existing_core = self._remove_preference_verbs(existing_norm)

            if new_core and new_core == existing_core:
                return "conflict_candidate"

        return "unique"
