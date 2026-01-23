"""
App Registry
Day 51 — Alias & executable resolution ONLY.

Responsibilities:
- Map user-friendly names → OS executables OR URLs
- NO execution
- NO subprocess
- NO permissions
"""

class AppRegistry:
    # -------------------------------------------------
    # Canonical alias table (Linux-first executables)
    # -------------------------------------------------
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

    # -------------------------------------------------
    # Web destinations (opened via browser)
    # -------------------------------------------------
    _WEB_APPS = {
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
    }

    @classmethod
    def resolve(cls, app_name: str) -> str:
        """
        Resolve a user-facing app name to:
        - OS executable (for apps)
        - URL (for web destinations)

        Returns:
        - executable string OR URL
        - original name if unknown
        """

        if not app_name:
            return app_name

        key = app_name.strip().lower()

        # 🌐 Web apps take priority
        if key in cls._WEB_APPS:
            return cls._WEB_APPS[key]

        # 🖥️ Native applications
        return cls._ALIASES.get(key, key)
