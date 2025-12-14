from enum import Enum

class Intent(Enum):
    GREETING = "greeting"
    HELP = "help"
    EXIT = "exit"
    UNKNOWN = "unknown"

def detect_intent(tokens: list[str]) -> Intent:
    if not tokens:
        return Intent.UNKNOWN

    if any(t in ("hi", "hello", "hey") for t in tokens):
        return Intent.GREETING

    if any(t in ("help", "commands") for t in tokens):
        return Intent.HELP

    if any(t in ("exit", "quit", "bye") for t in tokens):
        return Intent.EXIT

    return Intent.UNKNOWN
