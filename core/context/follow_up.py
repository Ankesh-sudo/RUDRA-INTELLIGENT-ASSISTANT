"""
Follow-up Context Manager — INTENT ISOLATED (Day 15.1)

Fixes:
✔ Cross-intent argument pollution
✔ Unsafe replay between unrelated actions

Preserves:
✔ Day 12 execution model
✔ Day 13–14 follow-up behavior
✔ Additive, safe, reversible design
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class ReferenceType(Enum):
    PRONOUN = "pronoun"
    LOCATION = "location"
    ACTION = "action"
    OBJECT = "object"
    DEMONSTRATIVE = "demonstrative"


# ------------------------------------------------------------------
# INTENT → ALLOWED ENTITY KEYS (STRICT)
# ------------------------------------------------------------------
INTENT_ENTITY_WHITELIST: Dict[str, List[str]] = {
    "open_browser": ["url", "target"],
    "search_web": ["query", "target"],
    "open_file_manager": ["path", "target"],
    "list_files": ["path", "target"],
    "open_file": ["filename", "full_path", "target"],
    "open_terminal": ["command", "target"],
}


class FollowUpContext:
    """
    Intent-isolated follow-up context (Day 15.1)
    """

    def __init__(self, max_contexts: int = 10, context_timeout: int = 300):
        self.contexts: List[Dict[str, Any]] = []
        self.max_contexts = max_contexts
        self.context_timeout = context_timeout

        self.reference_patterns = {
            ReferenceType.PRONOUN: re.compile(r"\b(it|that|this)\b", re.IGNORECASE),
            ReferenceType.LOCATION: re.compile(r"\b(there|here)\b", re.IGNORECASE),
            ReferenceType.ACTION: re.compile(r"\b(do|open|search)\s+(it|that)\b", re.IGNORECASE),
            ReferenceType.OBJECT: re.compile(
                r"\b(the)\s+(file|folder|browser|terminal)\b", re.IGNORECASE
            ),
        }

        self.resolution_map = {
            "it": ["action", "object"],
            "that": ["action", "object"],
            "this": ["action", "object"],
            "there": ["location"],
            "here": ["location"],
            "the file": ["object"],
            "the folder": ["object"],
        }

    # ------------------------------------------------------------------
    # CONTEXT STORAGE (INTENT-ISOLATED)
    # ------------------------------------------------------------------

    def add_context(
        self,
        action: str,
        result: Dict[str, Any],
        user_input: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Store ONLY successful actions with STRICT intent isolation
        """
        if not result.get("success", False):
            return None

        intent = action
        raw_entities = result.get("entities", {})

        safe_entities = self._filter_entities_by_intent(intent, raw_entities)

        context = {
            "intent": intent,
            "action": action,
            "entities": safe_entities,
            "user_input": user_input,
            "timestamp": datetime.now(),
        }

        self.contexts.insert(0, context)

        if len(self.contexts) > self.max_contexts:
            self.contexts = self.contexts[: self.max_contexts]

        self._cleanup_old_contexts()
        return context

    # ------------------------------------------------------------------
    # CONTEXT RESOLUTION (INTENT SAFE)
    # ------------------------------------------------------------------

    def resolve_reference(self, text: str) -> Tuple[Optional[Dict[str, Any]], str]:
        self._cleanup_old_contexts()

        if not self.contexts:
            return None, "no_context"

        text_lower = text.lower().strip()

        for ref, allowed_types in self.resolution_map.items():
            if ref in text_lower:
                for ctx in self.contexts:
                    if self._context_matches_types(ctx, allowed_types):
                        return ctx, ref

        for ref_type, pattern in self.reference_patterns.items():
            if pattern.search(text_lower):
                return self.contexts[0], ref_type.value

        return None, "unresolved"

    # ------------------------------------------------------------------
    # ENTITY FILTERING (DAY 15.1 CORE FIX)
    # ------------------------------------------------------------------

    def _filter_entities_by_intent(
        self, intent: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Strip ALL entities not allowed for this intent
        """
        allowed_keys = INTENT_ENTITY_WHITELIST.get(intent, [])
        return {k: v for k, v in entities.items() if k in allowed_keys}

    # ------------------------------------------------------------------
    # MATCHING HELPERS
    # ------------------------------------------------------------------

    def _context_matches_types(self, context: Dict[str, Any], types: List[str]) -> bool:
        if "action" in types:
            return True
        if "object" in types and context.get("entities"):
            return True
        if "location" in types and "path" in context.get("entities", {}):
            return True
        return False

    # ------------------------------------------------------------------
    # CLEANUP & ACCESSORS
    # ------------------------------------------------------------------

    def _cleanup_old_contexts(self):
        now = datetime.now()
        self.contexts = [
            ctx
            for ctx in self.contexts
            if now - ctx["timestamp"] < timedelta(seconds=self.context_timeout)
        ]

    def get_last_context(self) -> Optional[Dict[str, Any]]:
        self._cleanup_old_contexts()
        return self.contexts[0] if self.contexts else None

    def clear_context(self):
        self.contexts.clear()
