"""
Follow-up Context Manager — INTENT ISOLATED (Day 15.3)

Adds:
✔ Cross-intent replay blocking
✔ Intent-class verification before replay

Preserves:
✔ Day 12 execution model
✔ Day 13–14 follow-up behavior
✔ Day 15.1 entity isolation
✔ Fully additive & reversible
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


# ------------------------------------------------------------------
# INTENT → INTENT CLASS (DAY 15)
# ------------------------------------------------------------------
INTENT_CLASS: Dict[str, str] = {
    "open_browser": "system",
    "search_web": "system",
    "open_file_manager": "filesystem",
    "list_files": "filesystem",
    "open_file": "filesystem",
    "open_terminal": "dangerous",
}


class FollowUpContext:
    """
    Intent-isolated follow-up context (Day 15.3)
    """

    def __init__(self, max_contexts: int = 10, context_timeout: int = 300):
        self.contexts: List[Dict[str, Any]] = []
        self.max_contexts = max_contexts
        self.context_timeout = context_timeout

        self.reference_patterns = {
            ReferenceType.PRONOUN: re.compile(r"\b(it|that|this|them)\b", re.IGNORECASE),
            ReferenceType.LOCATION: re.compile(r"\b(there|here)\b", re.IGNORECASE),
            ReferenceType.ACTION: re.compile(
                r"\b(open|search|list)\s+(it|that|them)\b", re.IGNORECASE
            ),
            ReferenceType.OBJECT: re.compile(
                r"\b(the)\s+(file|folder|browser|terminal)\b", re.IGNORECASE
            ),
        }

        self.resolution_map = {
            "it": ["action", "object"],
            "that": ["action", "object"],
            "this": ["action", "object"],
            "them": ["action", "object"],
            "there": ["location"],
            "here": ["location"],
            "the file": ["object"],
            "the folder": ["object"],
        }

    # ------------------------------------------------------------------
    # CONTEXT STORAGE (INTENT + ENTITY SAFE)
    # ------------------------------------------------------------------

    def add_context(
        self,
        action: str,
        result: Dict[str, Any],
        user_input: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Store ONLY successful actions with strict intent isolation
        """
        if not result.get("success", False):
            return None

        intent = action
        raw_entities = result.get("entities", {})

        safe_entities = self._filter_entities_by_intent(intent, raw_entities)

        context = {
            "intent": intent,
            "action": action,
            "intent_class": INTENT_CLASS.get(intent),
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
    # CONTEXT RESOLUTION (DAY 15.3 SAFE)
    # ------------------------------------------------------------------

    def resolve_reference(self, text: str) -> Tuple[Optional[Dict[str, Any]], str]:
        self._cleanup_old_contexts()

        if not self.contexts:
            return None, "no_context"

        text_lower = text.lower().strip()

        # --------------------------------------------------
        # Detect reference first
        # --------------------------------------------------
        reference_found = False
        for pattern in self.reference_patterns.values():
            if pattern.search(text_lower):
                reference_found = True
                break

        if not reference_found:
            return None, "no_reference"

        # Candidate = most recent context ONLY
        candidate = self.contexts[0]

        # --------------------------------------------------
        # 🔒 DAY 15.3 — CROSS-INTENT BLOCK
        # --------------------------------------------------
        inferred_class = self._infer_intent_class_from_text(text_lower)
        stored_class = candidate.get("intent_class")

        if inferred_class and stored_class and inferred_class != stored_class:
            return None, "cross_intent_blocked"

        return candidate, "resolved"

    # ------------------------------------------------------------------
    # ENTITY FILTERING (DAY 15.1 CORE FIX)
    # ------------------------------------------------------------------

    def _filter_entities_by_intent(
        self, intent: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        allowed_keys = INTENT_ENTITY_WHITELIST.get(intent, [])
        return {k: v for k, v in entities.items() if k in allowed_keys}

    # ------------------------------------------------------------------
    # INTENT CLASS INFERENCE (VERY CONSERVATIVE)
    # ------------------------------------------------------------------

    def _infer_intent_class_from_text(self, text: str) -> Optional[str]:
        """
        Used ONLY to block cross-intent replay.
        Never used to execute actions.
        """

        if any(w in text for w in ("search", "find", "lookup")):
            return "system"

        if any(w in text for w in ("open", "launch")):
            return "system"

        if any(w in text for w in ("file", "files", "folder", "directory", "list")):
            return "filesystem"

        return None

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
