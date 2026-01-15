"""
App Registry
Day 51 — Alias & executable resolution ONLY.

Responsibilities:
- Map user-friendly names → OS executables
- NO execution
- NO subprocess
- NO permissions
"""

class AppRegistry:
    # Canonical alias table (Linux-first)
    _ALIASES = {
        # Browsers
        "chrome": "google-chrome",
        "google chrome": "google-chrome",
        "chromium": "chromium",
        "firefox": "firefox",

        # Editors / IDEs
        "vscode": "code",
        "vs code": "code",
        "code": "code",

        # System tools
        "terminal": "gnome-terminal",
        "cmd": "gnome-terminal",
        "file manager": "nautilus",
        "files": "nautilus",
        "calculator": "gnome-calculator",
    }

    @classmethod
    def resolve(cls, app_name: str) -> str:
        """
        Resolve a user-facing app name to a real executable.

        Returns:
        - resolved executable string
        - or original name if unknown
        """

        if not app_name:
            return app_name

        key = app_name.strip().lower()
        return cls._ALIASES.get(key, key)
