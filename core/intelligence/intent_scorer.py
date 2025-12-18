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
    if not scores:
        return Intent.UNKNOWN, 0.0

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    return best_intent, best_score