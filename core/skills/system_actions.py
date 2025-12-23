import os
import re
from typing import Optional

from core.nlp.intent import Intent
from core.system.app_registry import AppRegistry

_registry = AppRegistry()
HOME_DIR = os.path.expanduser("~")


def handle(intent: Intent, raw_text: str) -> Optional[str]:
    """
    Day 11 system action dispatcher
    """
    text = raw_text.lower().strip()

    if intent == Intent.OPEN_BROWSER:
        return _open_browser(text)

    if intent == Intent.OPEN_FILE_MANAGER:
        return _open_file_manager(text)

    if intent == Intent.OPEN_TERMINAL:
        return _open_terminal()

    # Not a system action → let basic skills handle it
    return None


# ---------------- BROWSER ----------------

def _open_browser(text: str) -> str:
    url = _extract_url(text)

    if url:
        os.system(f"xdg-open {url} >/dev/null 2>&1 &")
        return f"Opening {url}"

    _registry.execute("browser")
    return "Opening browser"


def _extract_url(text: str) -> Optional[str]:
    COMMON = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com",
    }

    for key, url in COMMON.items():
        if key in text:
            return url

    match = re.search(r"(https?://\S+)", text)
    if match:
        return match.group(1)

    match = re.search(r"\b([\w\-]+\.(com|org|net|in))\b", text)
    if match:
        return "https://" + match.group(1)

    return None


# ---------------- FILE MANAGER ----------------

def _open_file_manager(text: str) -> str:
    folders = {
        "downloads": os.path.join(HOME_DIR, "Downloads"),
        "desktop": os.path.join(HOME_DIR, "Desktop"),
        "documents": os.path.join(HOME_DIR, "Documents"),
    }

    for key, path in folders.items():
        if key in text and os.path.exists(path):
            os.system(f"xdg-open {path} >/dev/null 2>&1 &")
            return f"Opening {key}"

    _registry.execute("file_manager")
    return "Opening file manager"


# ---------------- TERMINAL ----------------

def _open_terminal() -> str:
    _registry.execute("terminal")
    return "Opening terminal"
