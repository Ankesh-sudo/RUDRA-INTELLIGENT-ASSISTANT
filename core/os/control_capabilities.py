from enum import Enum


class OSControlCapability(str, Enum):
    """
    Declarative registry of allowed OS control capabilities.

    IMPORTANT:
    - This file defines WHAT is allowed, not HOW it is executed.
    - No OS calls.
    - No permissions enforced here.
    """

    # Window management
    WINDOW_FOCUS = "window_focus"
    WINDOW_MINIMIZE = "window_minimize"
    WINDOW_MAXIMIZE = "window_maximize"

    # Audio / display
    VOLUME_SET = "volume_set"
    BRIGHTNESS_SET = "brightness_set"

    # System utilities
    SCREENSHOT = "screenshot"
    CLIPBOARD_READ = "clipboard_read"
    SYSTEM_INFO_QUERY = "system_info_query"
