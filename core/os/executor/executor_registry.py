from enum import Enum
from typing import Dict

from core.os.control_capabilities import OSControlCapability


class ExecutorType(str, Enum):
    """
    Logical executor identifiers.

    DAY 63 — CAPABILITY → EXECUTOR BINDING (READ-ONLY)

    IMPORTANT:
    - These are NOT executor classes
    - These are NOT instantiated
    - These are labels / identities only
    """

    # Linux executors (logical)
    LINUX_BROWSER = "linux_browser"
    LINUX_APP = "linux_app"
    LINUX_TERMINAL = "linux_terminal"
    LINUX_MEDIA = "linux_media"
    LINUX_SYSTEM_INFO = "linux_system_info"

    # Stub / no-op executor (safe fallback)
    OS_CONTROL_STUB = "os_control_stub"


# -------------------------------------------------
# Capability → Executor mapping (DECLARATIVE ONLY)
# -------------------------------------------------

_CAPABILITY_EXECUTOR_MAP: Dict[OSControlCapability, ExecutorType] = {
    # -------------------------------------------------
    # Application & window control
    # -------------------------------------------------
    OSControlCapability.OPEN_APP: ExecutorType.LINUX_APP,
    OSControlCapability.CLOSE_APP: ExecutorType.LINUX_APP,

    OSControlCapability.WINDOW_FOCUS: ExecutorType.OS_CONTROL_STUB,
    OSControlCapability.WINDOW_MINIMIZE: ExecutorType.OS_CONTROL_STUB,
    OSControlCapability.WINDOW_MAXIMIZE: ExecutorType.OS_CONTROL_STUB,

    # -------------------------------------------------
    # Browser control
    # -------------------------------------------------
    OSControlCapability.OPEN_BROWSER: ExecutorType.LINUX_BROWSER,
    OSControlCapability.OPEN_URL: ExecutorType.LINUX_BROWSER,

    # -------------------------------------------------
    # Media control
    # -------------------------------------------------
    OSControlCapability.PLAY_MEDIA: ExecutorType.LINUX_MEDIA,
    OSControlCapability.PAUSE_MEDIA: ExecutorType.LINUX_MEDIA,
    OSControlCapability.RESUME_MEDIA: ExecutorType.LINUX_MEDIA,
    OSControlCapability.STOP_MEDIA: ExecutorType.LINUX_MEDIA,

    # -------------------------------------------------
    # Terminal control (sandboxed)
    # -------------------------------------------------
    OSControlCapability.OPEN_TERMINAL: ExecutorType.LINUX_TERMINAL,
    OSControlCapability.RUN_TERMINAL_COMMAND_SAFE: ExecutorType.LINUX_TERMINAL,

    # -------------------------------------------------
    # System information (read-only)
    # -------------------------------------------------
    OSControlCapability.SYSTEM_INFO_QUERY: ExecutorType.LINUX_SYSTEM_INFO,
    OSControlCapability.SCREENSHOT: ExecutorType.LINUX_SYSTEM_INFO,
    OSControlCapability.CLIPBOARD_READ: ExecutorType.LINUX_SYSTEM_INFO,
}


class ExecutorRegistry:
    """
    DAY 63 — EXECUTOR REGISTRY

    Read-only mapping from OS capability to executor identity.

    GUARANTEES:
    - No executor instantiation
    - No OS execution
    - No permission checks
    - Safe default fallback
    """

    @staticmethod
    def get_executor_type(
        capability: OSControlCapability,
    ) -> ExecutorType:
        """
        Return the executor type responsible for a capability.

        Unknown or unbound capabilities are safely routed
        to the OS_CONTROL_STUB.
        """
        return _CAPABILITY_EXECUTOR_MAP.get(
            capability,
            ExecutorType.OS_CONTROL_STUB,
        )
