"""
Follow-up Context Manager — INTENT ISOLATED + REPLAY SAFE (Day 15.4 FINAL)

Fixes:
✔ Correct filesystem → filesystem replay
✔ Correct cross-intent blocking
✔ Replay rate limiting
✔ Follow-up TTL hardening
✔ Intent-isolated entity replay

Fully aligned with test_day15_all_edge_cases.py
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
# INTENT → INTENT CLASS
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
    Intent-isolated follow-up context with replay hardening (Day 15.4)
    """

    def __init__(
        self,
        max_contexts: int = 10,
        context_timeout: int = 300,
        max_replays: int = 3,
        replay_window: int = 30,
    ):
        self.contexts: List[Dict[str, Any]] = []
        self.max_contexts = max_contexts
        self.context_timeout = context_timeout

        # Replay protection
        self.max_replays = max_replays
        self.replay_window = replay_window

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

    # ------------------------------------------------------------------
    # CONTEXT STORAGE
    # ------------------------------------------------------------------

    def add_context(
        self,
        action: str,
        result: Dict[str, Any],
        user_input: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        if not result.get("success", False):
            return None

        safe_entities = self._filter_entities_by_intent(
            action, result.get("entities", {})
        )

        context = {
            "intent": action,
            "action": action,
            "intent_class": INTENT_CLASS.get(action),
            "entities": safe_entities,
            "user_input": user_input,
            "timestamp": datetime.now(),
            "replay_count": 0,
            "last_replay": None,
        }

        self.contexts.insert(0, context)
        self.contexts = self.contexts[: self.max_contexts]

        self._cleanup_old_contexts()
        return context

    # ------------------------------------------------------------------
    # CONTEXT RESOLUTION (DAY 15.4 FINAL)
    # ------------------------------------------------------------------

    def resolve_reference(self, text: str) -> Tuple[Optional[Dict[str, Any]], str]:
        self._cleanup_old_contexts()

        if not self.contexts:
            return None, "no_context"

        text_lower = text.lower().strip()

        # Must contain a reference word
        if not any(p.search(text_lower) for p in self.reference_patterns.values()):
            return None, "no_reference"

        candidate = self.contexts[0]

        # --------------------------------------------------
        # 🔒 Cross-intent replay blocking
        # --------------------------------------------------
        inferred_class = self._infer_intent_class_from_text(text_lower)
        stored_class = candidate.get("intent_class")

        if inferred_class and stored_class and inferred_class != stored_class:
            return None, "cross_intent_blocked"

        # --------------------------------------------------
        # 🔒 ACTION MISMATCH BLOCK (ENTITY LEAK PREVENTION)
        # --------------------------------------------------
        stored_action = candidate.get("action")
        if stored_action:
            expected_verb = stored_action.split("_")[0]  # open / list / search
            if not text_lower.startswith(expected_verb):
                return None, "action_mismatch"

        # --------------------------------------------------
        # 🔒 Replay rate limiting
        # --------------------------------------------------
        if not self._is_replay_allowed(candidate):
            return None, "replay_limited"

        self._mark_replay(candidate)
        return candidate, "resolved"

    # ------------------------------------------------------------------
    # REPLAY CONTROL
    # ------------------------------------------------------------------

    def _is_replay_allowed(self, context: Dict[str, Any]) -> bool:
        if context["replay_count"] >= self.max_replays:
            return False

        last = context.get("last_replay")
        if not last:
            return True

        return (datetime.now() - last) < timedelta(seconds=self.replay_window)

    def _mark_replay(self, context: Dict[str, Any]):
        context["replay_count"] += 1
        context["last_replay"] = datetime.now()

    # ------------------------------------------------------------------
    # ENTITY FILTERING
    # ------------------------------------------------------------------

    def _filter_entities_by_intent(
        self, intent: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        allowed_keys = INTENT_ENTITY_WHITELIST.get(intent, [])
        return {k: v for k, v in entities.items() if k in allowed_keys}

    # ------------------------------------------------------------------
    # CONSERVATIVE INTENT CLASS INFERENCE (BLOCKING ONLY)
    # ------------------------------------------------------------------

    def _infer_intent_class_from_text(self, text: str) -> Optional[str]:
        """
        Used ONLY to block cross-intent replay.

        Ambiguous commands like:
        - "open it again"
        return None → allowed

        Explicit domain words block mismatches.
        """

        if any(w in text for w in ("browser", "search", "web", "url", "google")):
            return "system"

        if any(w in text for w in ("file", "files", "folder", "directory", "list")):
            return "filesystem"

        return None

    # ------------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------------

    def _cleanup_old_contexts(self):
        now = datetime.now()
        self.contexts = [
            ctx
            for ctx in self.contexts
            if now - ctx["timestamp"] < timedelta(seconds=self.context_timeout)
        ]

    def clear_context(self):
        self.contexts.clear()
