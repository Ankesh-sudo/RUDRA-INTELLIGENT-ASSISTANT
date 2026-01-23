import subprocess


class AppControl:
    """
    DAY 64 — SAFE APPLICATION CONTROL (LINUX)

    Guarantees:
    - Desktop-level app launch only
    - No shell execution
    - No terminal semantics
    - No privilege escalation
    """

    @staticmethod
    def open_app(app_name: str) -> None:
        """
        Open an installed desktop application using its .desktop entry.

        Examples:
        - "firefox"
        - "google-chrome"
        - "org.gnome.Calculator"

        Rules:
        - App name only (no paths)
        - No shell=True
        - User-level execution only
        """
        if not app_name:
            raise ValueError("Application name is required")

        if "/" in app_name or app_name.strip() != app_name:
            raise ValueError("Invalid application name")

        subprocess.Popen(
            ["gtk-launch", app_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
