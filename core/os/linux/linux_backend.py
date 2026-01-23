import webbrowser

from core.os.linux.app_control import AppControl


class LinuxBackend:
    """
    DAY 64 — LINUX OS BACKEND (LEVEL 1)

    Responsibilities:
    - Perform SAFE, REAL OS actions
    - NO intent logic
    - NO permission logic
    - NO terminal execution
    - NO file operations

    Enabled TODAY:
    - OPEN_BROWSER
    - OPEN_URL (whitelisted)
    - OPEN_APP
    """

    # -------------------------------------------------
    # Browser control (SAFE)
    # -------------------------------------------------

    _ALLOWED_URLS = {
        "https://www.google.com",
        "https://www.youtube.com",
        "https://github.com",
    }

    @staticmethod
    def open_browser() -> None:
        """
        Open the system default browser.
        """
        webbrowser.open("https://www.google.com", new=1)

    @staticmethod
    def open_url(url: str) -> None:
        """
        Open a whitelisted URL only.
        """
        if not url or url not in LinuxBackend._ALLOWED_URLS:
            raise ValueError("URL not allowed")

        webbrowser.open(url, new=1)

    # -------------------------------------------------
    # Application control (SAFE)
    # -------------------------------------------------

    @staticmethod
    def open_application(app_name: str) -> None:
        """
        Open a desktop application using .desktop entry.
        """
        AppControl.open_app(app_name)

    # -------------------------------------------------
    # Disabled paths (explicit)
    # -------------------------------------------------

    @staticmethod
    def run(*args, **kwargs):
        """
        Disabled on Day 64.

        Generic execution is NOT allowed yet.
        Terminal / command execution starts on Day 67.
        """
        raise RuntimeError(
            "LinuxBackend.run is disabled on Day 64 "
            "(generic execution not allowed)"
        )
