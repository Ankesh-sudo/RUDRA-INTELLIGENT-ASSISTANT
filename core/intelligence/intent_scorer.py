from typing import Dict, List
from core.nlp.intent import Intent


# -------------------------------------------------
# Day 14.4 — Verb aliases (kept)
# -------------------------------------------------
VERB_ALIASES: Dict[str, Intent] = {
    # Search intent
    "search": Intent.SEARCH_WEB,
    "find": Intent.SEARCH_WEB,
    "lookup": Intent.SEARCH_WEB,
    "look": Intent.SEARCH_WEB,

    # Open intent (generic)
    "open": Intent.OPEN_BROWSER,
    "launch": Intent.OPEN_BROWSER,
    "start": Intent.OPEN_BROWSER,
}


# -------------------------------------------------
# Day 15.1 — HARD INTENT GUARDS (CRITICAL)
# -------------------------------------------------
HARD_GUARDS: Dict[str, Intent] = {
    # Terminal must never be browser
    "terminal": Intent.OPEN_TERMINAL,
    "console": Intent.OPEN_TERMINAL,
    "shell": Intent.OPEN_TERMINAL,

    # File operations
    "file": Intent.OPEN_FILE,

    # Listing intent
    "list": Intent.LIST_FILES,
}


# -------------------------------------------------
# Day 15.2 — INTENT PRIORITY (TIE-BREAKER)
# -------------------------------------------------
INTENT_PRIORITY: Dict[Intent, int] = {
    Intent.OPEN_TERMINAL: 5,
    Intent.OPEN_FILE: 4,
    Intent.LIST_FILES: 4,
    Intent.OPEN_FILE_MANAGER: 3,
    Intent.SEARCH_WEB: 3,
    Intent.OPEN_BROWSER: 2,
    Intent.GREETING: 1,
    Intent.HELP: 1,
    Intent.EXIT: 1,
}


# -------------------------------------------------
# Keyword evidence per intent
# -------------------------------------------------
INTENT_KEYWORDS: Dict[Intent, List[str]] = {
    # Core
    Intent.GREETING: ["hi", "hello", "hey"],
    Intent.HELP: ["help", "commands"],
    Intent.EXIT: ["exit", "quit", "bye"],

    # Notes
    Intent.NOTE_CREATE: ["note", "save", "write", "take"],
    Intent.NOTE_READ: ["read", "show"],

    # --------------------
    # System actions
    # --------------------
    Intent.OPEN_BROWSER: [
        "browser",
        "chrome",
        "firefox",
        "internet",
        "youtube",
        "google",
        "github",
        "website",
        "site",
    ],

    Intent.OPEN_TERMINAL: [
        "terminal",
        "console",
        "shell",
    ],

    Intent.OPEN_FILE_MANAGER: [
        "folder",
        "directory",
        "downloads",
        "download",
        "desktop",
        "documents",
    ],

    Intent.OPEN_FILE: [
        "file",
    ],

    Intent.LIST_FILES: [
        "list",
        "files",
    ],

    Intent.SEARCH_WEB: [
        "search",
        "find",
        "lookup",
        "query",
    ],
}


def score_intents(tokens: List[str]) -> Dict[Intent, int]:
    """
    Day 15 scoring pipeline:
    1. Hard guards
    2. Keyword matches
    3. Verb alias boost
    4. Action boost (restricted)
    """
    scores: Dict[Intent, int] = {i: 0 for i in Intent}

    # -------------------------------------------------
    # 1️⃣ HARD GUARDS (highest impact)
    # -------------------------------------------------
    for token in tokens:
        if token in HARD_GUARDS:
            scores[HARD_GUARDS[token]] += 3

    # -------------------------------------------------
    # 2️⃣ Keyword matching
    # -------------------------------------------------
    for intent, keywords in INTENT_KEYWORDS.items():
        for token in tokens:
            if token in keywords:
                scores[intent] += 1

    # -------------------------------------------------
    # 3️⃣ Verb alias boosting
    # -------------------------------------------------
    for token in tokens:
        alias_intent = VERB_ALIASES.get(token)
        if alias_intent:
            scores[alias_intent] += 1

    # -------------------------------------------------
    # 4️⃣ Action verb boost (RESTRICTED)
    # -------------------------------------------------
    if "open" in tokens or "launch" in tokens or "start" in tokens:
        for intent in (
            Intent.OPEN_TERMINAL,
            Intent.OPEN_FILE,
            Intent.OPEN_FILE_MANAGER,
            Intent.OPEN_BROWSER,
        ):
            if scores[intent] > 0:
                scores[intent] += 1

    return scores


def pick_best_intent(scores: Dict[Intent, int], tokens: List[str]):
    """
    Day 15 intent selection with priority tie-breaking
    and calibrated confidence.
    """
    if not scores:
        return Intent.UNKNOWN, 0.0

    best_score = max(scores.values())
    if best_score == 0:
        return Intent.UNKNOWN, 0.0

    # All intents with same top score
    candidates = [i for i, s in scores.items() if s == best_score]

    # -------------------------------------------------
    # Day 15.2 — Priority-based tie break
    # -------------------------------------------------
    best_intent = max(
        candidates,
        key=lambda i: INTENT_PRIORITY.get(i, 0)
    )

    # EXIT is always confident
    if best_intent == Intent.EXIT:
        return Intent.EXIT, 1.0

    # -------------------------------------------------
    # Day 15.3 — Confidence recalibration
    # -------------------------------------------------
    confidence = min(
        1.0,
        (best_score + INTENT_PRIORITY.get(best_intent, 0)) / (len(tokens) + 2)
    )

    return best_intent, confidence
