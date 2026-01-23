"""
Permission scope definitions.

Rules:
- ALL_SCOPES is the single source of truth
- Canonical scopes are UPPER_SNAKE_CASE
- Scopes represent *capabilities*, not intents
- Safe UI actions must NOT require permission
"""

# -------------------------------------------------
# 🔐 Canonical scopes (DANGEROUS / PRIVILEGED ONLY)
# -------------------------------------------------

# Terminal / shell / command execution
TERMINAL_EXEC = "TERMINAL_EXEC"

# File system (destructive or sensitive)
FILE_READ = "FILE_READ"
FILE_DELETE = "FILE_DELETE"

# System / OS-level control (broad)
SYSTEM_CONTROL = "SYSTEM_CONTROL"

# Network-level operations (future-safe)
NETWORK_CONTROL = "NETWORK_CONTROL"

# Screen / capture (privacy-sensitive)
SCREEN_CAPTURE = "SCREEN_CAPTURE"

# -------------------------------------------------
# 🧭 Day 61 — OS CONTROL (FINE-GRAINED, DECLARATIVE)
# -------------------------------------------------
# These scopes are defined now but NOT yet enforced
# by PermissionEvaluator until later Phase 9 days.

OS_WINDOW_CONTROL = "OS_WINDOW_CONTROL"
OS_AUDIO_CONTROL = "OS_AUDIO_CONTROL"
OS_DISPLAY_CONTROL = "OS_DISPLAY_CONTROL"
OS_SYSTEM_READ = "OS_SYSTEM_READ"

# -------------------------------------------------
# 🟢 Explicitly SAFE scopes (NON-PRIVILEGED)
# -------------------------------------------------
# These exist for semantic clarity only.
# They are NOT enforced by PermissionEvaluator.

GUI_APP_LAUNCH = "GUI_APP_LAUNCH"
SYSTEM_INFO = "SYSTEM_INFO"

# -------------------------------------------------
# 🔁 Backward-compat / alias normalization
# -------------------------------------------------
# Aliases are NEVER added directly to ALL_SCOPES.

SCOPE_ALIASES = {
    # file operations
    "filesystem.read": FILE_READ,
    "filesystem.delete": FILE_DELETE,
    "file.read": FILE_READ,
    "file.delete": FILE_DELETE,

    # terminal / shell
    "terminal": TERMINAL_EXEC,
    "shell": TERMINAL_EXEC,

    # legacy lowercase
    "file_read": FILE_READ,
    "file_delete": FILE_DELETE,

    # OS control (future-facing aliases)
    "os.window.control": OS_WINDOW_CONTROL,
    "os.audio.control": OS_AUDIO_CONTROL,
    "os.display.control": OS_DISPLAY_CONTROL,
    "os.system.read": OS_SYSTEM_READ,
}

# -------------------------------------------------
# 📌 Registry (ENFORCED SCOPES ONLY)
# -------------------------------------------------
# NOTE:
# OS_* scopes are INCLUDED but not yet ACTIVELY USED
# until Day 62+ evaluator wiring.

ALL_SCOPES = {
    TERMINAL_EXEC,
    FILE_READ,
    FILE_DELETE,
    SYSTEM_CONTROL,
    NETWORK_CONTROL,
    SCREEN_CAPTURE,

    # Day 61 OS control scopes
    OS_WINDOW_CONTROL,
    OS_AUDIO_CONTROL,
    OS_DISPLAY_CONTROL,
    OS_SYSTEM_READ,
}

# -------------------------------------------------
# 🧩 LEGACY EXPORTS (REQUIRED FOR LOCKED TESTS)
# -------------------------------------------------
# These are aliases ONLY.
# They do NOT expand permission surface.

# Older tests expect APP_CONTROL to exist
APP_CONTROL = SYSTEM_CONTROL
