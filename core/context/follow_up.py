"""
Follow-up Context Manager - SAFE VERSION (Day 13.1)

Handles contextual references like:
- "it", "that", "this"
- "there", "here"

DESIGN GOALS:
✔ Does NOT break Day 12
✔ Stores ONLY successful actions
✔ No OS inference
✔ No intent override
✔ Additive & reversible
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class ReferenceType(Enum):
    """Types of contextual references"""
    PRONOUN = "pronoun"
    LOCATION = "location"
    ACTION = "action"
    OBJECT = "object"
    DEMONSTRATIVE = "demonstrative"


class FollowUpContext:
    """
    SAFE Follow-up Context Manager

    Responsibilities:
    - Store recent successful actions
    - Resolve simple references ("it", "that", "there")
    - NEVER interfere with normal execution
    """

    def __init__(self, max_contexts: int = 10, context_timeout: int = 300):
        self.contexts: List[Dict[str, Any]] = []
        self.max_contexts = max_contexts
        self.context_timeout = context_timeout

        # SAFE reference detection patterns
        self.reference_patterns = {
            ReferenceType.PRONOUN: re.compile(r"\b(it|that|this)\b", re.IGNORECASE),
            ReferenceType.LOCATION: re.compile(r"\b(there|here)\b", re.IGNORECASE),
            ReferenceType.ACTION: re.compile(r"\b(do|open|search)\s+(it|that)\b", re.IGNORECASE),
            ReferenceType.OBJECT: re.compile(r"\b(the)\s+(file|folder|browser|terminal)\b", re.IGNORECASE),
        }

        # SAFE resolution rules (Day 12 compatible only)
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
    # CONTEXT STORAGE
    # ------------------------------------------------------------------

    def add_context(
        self,
        action: str,
        result: Dict[str, Any],
        user_input: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Store context ONLY if action succeeded
        """
        if not result.get("success", False):
            return None

        context = {
            "action": action,
            "result": result,
            "user_input": user_input,
            "timestamp": datetime.now(),
            "entities": self._extract_safe_entities(result),
        }

        self.contexts.insert(0, context)

        if len(self.contexts) > self.max_contexts:
            self.contexts = self.contexts[: self.max_contexts]

        self._cleanup_old_contexts()
        return context

    # ------------------------------------------------------------------
    # CONTEXT RESOLUTION
    # ------------------------------------------------------------------

    def resolve_reference(self, text: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Resolve references safely.
        Returns (context, reference_type)
        """
        self._cleanup_old_contexts()

        if not self.contexts:
            return None, "no_context"

        text_lower = text.lower().strip()

        # Explicit phrase resolution
        for ref, allowed_types in self.resolution_map.items():
            if ref in text_lower:
                for ctx in self.contexts:
                    if self._context_matches_types(ctx, allowed_types):
                        return ctx, ref

        # Pattern-based resolution
        for ref_type, pattern in self.reference_patterns.items():
            if pattern.search(text_lower):
                return self.contexts[0], ref_type.value

        return None, "unresolved"

    # ------------------------------------------------------------------
    # SAFE ENTITY EXTRACTION
    # ------------------------------------------------------------------

    def _extract_safe_entities(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract ONLY entities that Day 12 already produces
        """
        entities = {"type": "general"}

        result_data = result.get("result", {}) if isinstance(result, dict) else {}

        if "url" in result_data:
            entities["type"] = "website"
            entities["url"] = result_data["url"]
            entities["target"] = result_data.get("target", "website")

        if "path" in result_data:
            entities["type"] = "path"
            entities["path"] = result_data["path"]
            entities["target"] = result_data.get("target", "path")

        if "query" in result_data:
            entities["type"] = "search"
            entities["query"] = result_data["query"]

        return entities

    # ------------------------------------------------------------------
    # MATCHING HELPERS (SAFE)
    # ------------------------------------------------------------------

    def _context_matches_types(self, context: Dict[str, Any], types: List[str]) -> bool:
        entity_type = context.get("entities", {}).get("type", "general")

        for t in types:
            if t == "action":
                return True
            if t == "object" and entity_type in ("website", "path"):
                return True
            if t == "location" and entity_type in ("website", "path"):
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

    def get_last_action(self) -> Optional[Dict[str, Any]]:
        self._cleanup_old_contexts()
        return self.contexts[0] if self.contexts else None

    def clear_context(self):
        self.contexts.clear()
