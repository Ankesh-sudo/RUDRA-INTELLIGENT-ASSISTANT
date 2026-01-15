from typing import Dict, List
from core.nlp.intent import Intent

# -------------------------------------------------
# Verb aliases (Day 50 – FINAL)
# -------------------------------------------------
VERB_ALIASES: Dict[str, Intent] = {
    # App / OS control
    "open": Intent.OPEN_APP,
    "launch": Intent.OPEN_APP,
    "start": Intent.OPEN_APP,
    "run": Intent.OPEN_APP,

    # Search
    "search": Intent.SEARCH_WEB,
    "find": Intent.SEARCH_WEB,
    "lookup": Intent.SEARCH_WEB,
}

# -------------------------------------------------
# HARD GUARDS (authoritative overrides)
# -------------------------------------------------
HARD_GUARDS: Dict[str, Intent] = {
    # Terminal must never be treated as browser/app
    "terminal": Intent.OPEN_TERMINAL,
    "console": Intent.OPEN_TERMINAL,
    "shell": Intent.OPEN_TERMINAL,

    # System info
    "system": Intent.SYSTEM_INFO,
    "info": Intent.SYSTEM_INFO,

    # Listing
    "list": Intent.LIST_FILES,
    "files": Intent.LIST_FILES,
}

# -------------------------------------------------
# INTENT PRIORITY (tie-breaker)
# -------------------------------------------------
INTENT_PRIORITY: Dict[Intent, int] = {
    Intent.OPEN_TERMINAL: 6,      # highest risk
    Intent.OPEN_APP: 5,
    Intent.SYSTEM_INFO: 5,

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
# KEYWORD EVIDENCE
# -------------------------------------------------
INTENT_KEYWORDS: Dict[Intent, List[str]] = {
    # Core
    Intent.GREETING: ["hi", "hello", "hey"],
    Intent.HELP: ["help", "commands"],
    Intent.EXIT: ["exit", "quit", "bye"],

    # System info
    Intent.SYSTEM_INFO: [
        "system", "info", "details", "status"
    ],

    # Open app (apps + verbs)
    Intent.OPEN_APP: [
        "open", "launch", "start", "run",
        "chrome", "firefox", "github", "youtube",
        "calculator", "terminal"
    ],

    # Search
    Intent.SEARCH_WEB: [
        "search", "find", "lookup", "query"
    ],

    # Files
    Intent.LIST_FILES: [
        "list", "files"
    ],
}

# -------------------------------------------------
# SCORING
# -------------------------------------------------
def score_intents(tokens: List[str]) -> Dict[Intent, int]:
    scores: Dict[Intent, int] = {i: 0 for i in Intent}

    # 1) Hard guards (highest impact)
    for t in tokens:
        if t in HARD_GUARDS:
            scores[HARD_GUARDS[t]] += 3

    # 2) Keyword evidence
    for intent, keywords in INTENT_KEYWORDS.items():
        for t in tokens:
            if t in keywords:
                scores[intent] += 1

    # 3) Verb aliases
    for t in tokens:
        if t in VERB_ALIASES:
            scores[VERB_ALIASES[t]] += 1

    return scores


def pick_best_intent(scores: Dict[Intent, int], tokens: List[str]):
    best_score = max(scores.values(), default=0)
    if best_score == 0:
        return Intent.UNKNOWN, 0.0

    candidates = [i for i, s in scores.items() if s == best_score]
    best_intent = max(candidates, key=lambda i: INTENT_PRIORITY.get(i, 0))

    if best_intent == Intent.EXIT:
        return best_intent, 1.0

    confidence = min(
        1.0,
        (best_score + INTENT_PRIORITY.get(best_intent, 0)) / (len(tokens) + 2)
    )

    return best_intent, confidence
