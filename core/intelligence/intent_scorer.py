from typing import Dict, List
from core.nlp.intent import Intent

# Keyword evidence per intent (language-agnostic at core level)
INTENT_KEYWORDS: Dict[Intent, List[str]] = {
    Intent.GREETING: ["hi", "hello", "hey"],
    Intent.HELP: ["help", "commands"],
    Intent.EXIT: ["exit", "quit", "bye"],
    Intent.NOTE_CREATE: ["note", "save", "write", "take"],
    Intent.NOTE_READ: ["read", "show", "list"],
}

def score_intents(tokens: List[str]) -> Dict[Intent, int]:
    scores: Dict[Intent, int] = {i: 0 for i in Intent}

    for intent, kws in INTENT_KEYWORDS.items():
        for t in tokens:
            if t in kws:
                scores[intent] += 1

    return scores

def pick_best_intent(scores, tokens):
    # Explicit priority rules (override scoring)
    if "read" in tokens or "show" in tokens or "list" in tokens:
        return Intent.NOTE_READ

    if "save" in tokens or "write" in tokens or "take" in tokens:
        return Intent.NOTE_CREATE

    # Fallback to scoring
    best_intent, best_score = Intent.UNKNOWN, 0
    for intent, score in scores.items():
        if score > best_score:
            best_intent, best_score = intent, score

    return best_intent if best_score > 0 else Intent.UNKNOWN