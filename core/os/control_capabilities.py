from enum import Enum


class OSControlCapability(str, Enum):
    """
    Declarative registry of allowed OS control capabilities.

    DAY 62 — CAPABILITY REGISTRY (FOUNDATION)

    IMPORTANT GUARANTEES:
    - Declarative only (WHAT, not HOW)
    - No OS execution
    - No permissions enforced
    - Backward-compatible with Day 61 contracts
    """

    # -------------------------------------------------
    # Window management (LEGACY — DAY 61 REQUIRED)
    # -------------------------------------------------

    WINDOW_FOCUS = "window_focus"
    WINDOW_MINIMIZE = "window_minimize"
    WINDOW_MAXIMIZE = "window_maximize"

    # -------------------------------------------------
    # Window management (FUTURE-FRIENDLY ALIASES)
    # -------------------------------------------------

    FOCUS_WINDOW = "window_focus"
    MINIMIZE_WINDOW = "window_minimize"
    MAXIMIZE_WINDOW = "window_maximize"

    # -------------------------------------------------
    # Application control
    # -------------------------------------------------

    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"

    # -------------------------------------------------
    # Browser control
    # -------------------------------------------------

    OPEN_BROWSER = "open_browser"
    OPEN_URL = "open_url"

    # -------------------------------------------------
    # Media control (safe)
    # -------------------------------------------------

    PLAY_MEDIA = "play_media"
    PAUSE_MEDIA = "pause_media"
    RESUME_MEDIA = "resume_media"
    STOP_MEDIA = "stop_media"

    # -------------------------------------------------
    # Audio / display (capped)
    # -------------------------------------------------

    SET_VOLUME = "set_volume"
    SET_BRIGHTNESS = "set_brightness"

    # -------------------------------------------------
    # Terminal control (sandboxed)
    # -------------------------------------------------

    OPEN_TERMINAL = "open_terminal"
    RUN_TERMINAL_COMMAND_SAFE = "run_terminal_command_safe"

    # -------------------------------------------------
    # System info (read-only)
    # -------------------------------------------------

    SYSTEM_INFO_QUERY = "system_info_query"
    SCREENSHOT = "screenshot"
    CLIPBOARD_READ = "clipboard_read"

    # -------------------------------------------------
    # Internal / introspection
    # -------------------------------------------------

    LIST_CAPABILITIES = "list_capabilities"
