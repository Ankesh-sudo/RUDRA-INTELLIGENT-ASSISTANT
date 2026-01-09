"""
Context Pack Builder

Builds a safe, minimal context object
from STM and LTM for decision support.
"""

from core.memory.short_term_memory import ShortTermMemory
from core.memory.long_term_memory import LongTermMemory


class ContextPackBuilder:
    def __init__(self):
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()

    def build(self, *, intent: str | None = None) -> dict:
        """
        Build context pack for current interaction.
        """

        context = {
            "recent_conversation": [],
            "user_facts": [],
            "user_preferences": [],
        }

        # STM — last few turns
        context["recent_conversation"] = self.stm.fetch_recent(limit=5)

        # LTM — selective, rule-based
        context["user_facts"] = self.ltm.fetch_by_type("user_fact")
        context["user_preferences"] = self.ltm.fetch_by_type("user_preference")

        return context
