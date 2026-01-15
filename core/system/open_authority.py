"""
Open Authority
Day 52 — Decides whether an OPEN request targets an APP or the BROWSER.

Single responsibility:
- classify target as APP or BROWSER
"""

from enum import Enum


class OpenTarget(Enum):
    APP = "app"
    BROWSER = "browser"


class OpenAuthority:
    # Known web-first entities
    _WEB_ENTITIES = {
        "youtube",
        "google",
        "github",
        "gmail",
        "chatgpt",
        "netflix",
        "spotify",
        "facebook",
        "twitter",
        "x",
        "instagram",
    }

    # Known app-first entities
    _APP_ENTITIES = {
        "chrome",
        "chromium",
        "firefox",
        "vscode",
        "calculator",
        "terminal",
        "files",
        "file manager",
    }

    @classmethod
    def decide(cls, name: str) -> OpenTarget:
        if not name:
            return OpenTarget.APP  # safe default

        key = name.strip().lower()

        if key in cls._WEB_ENTITIES:
            return OpenTarget.BROWSER

        if key in cls._APP_ENTITIES:
            return OpenTarget.APP

        # Fallback rule:
        # unknown names open as apps (safer than web)
        return OpenTarget.APP
