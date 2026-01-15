from enum import Enum


class Intent(Enum):
    GREETING = "greeting"
    HELP = "help"
    EXIT = "exit"

    NOTE_CREATE = "note_create"
    NOTE_READ = "note_read"

    OPEN_BROWSER = "open_browser"
    OPEN_TERMINAL = "open_terminal"
    OPEN_FILE_MANAGER = "open_file_manager"
    OPEN_FILE = "open_file"
    SEARCH_WEB = "search_web"
    PLAY_MEDIA = "play_media"
    CONTROL_VOLUME = "control_volume"
    LIST_FILES = "list_files"

    # 🟦 Day 50 — OS control intents
    OPEN_APP = "open_app"
    SYSTEM_INFO = "system_info"

    UNKNOWN = "unknown"


def detect_intent(tokens: list[str]) -> Intent:
    if not tokens:
        return Intent.UNKNOWN

    # ---------------- BASIC ----------------
    if any(t in ("hi", "hello", "hey") for t in tokens):
        return Intent.GREETING

    if any(t in ("help", "commands") for t in tokens):
        return Intent.HELP

    if any(t in ("exit", "quit", "bye") for t in tokens):
        return Intent.EXIT

    # ---------------- NOTES ----------------
    if "note" in tokens and any(t in ("save", "write", "take") for t in tokens):
        return Intent.NOTE_CREATE

    if "note" in tokens and any(t in ("read", "show", "list") for t in tokens):
        return Intent.NOTE_READ

    # ---------------- DAY 50: SYSTEM INFO ----------------
    if "system" in tokens and "info" in tokens:
        return Intent.SYSTEM_INFO

    if "uname" in tokens or ("system" in tokens and "details" in tokens):
        return Intent.SYSTEM_INFO

    # ---------------- DAY 50: OPEN APP ----------------
    if any(t in ("open", "launch", "start") for t in tokens):
        # guard: avoid browser/web intents
        if "browser" not in tokens and "web" not in tokens:
            return Intent.OPEN_APP

    # ---------------- LEGACY ----------------
    if "browser" in tokens:
        return Intent.OPEN_BROWSER

    if "terminal" in tokens:
        return Intent.OPEN_TERMINAL

    if "file" in tokens and "manager" in tokens:
        return Intent.OPEN_FILE_MANAGER

    if "file" in tokens and any(t in ("open", "read") for t in tokens):
        return Intent.OPEN_FILE

    if "search" in tokens:
        return Intent.SEARCH_WEB

    if "list" in tokens and "files" in tokens:
        return Intent.LIST_FILES

    return Intent.UNKNOWN
