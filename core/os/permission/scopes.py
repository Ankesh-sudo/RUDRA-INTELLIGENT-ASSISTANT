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

# System / OS-level control
SYSTEM_CONTROL = "SYSTEM_CONTROL"

# Network-level operations (future-safe)
NETWORK_CONTROL = "NETWORK_CONTROL"

# Screen / capture (privacy-sensitive)
SCREEN_CAPTURE = "SCREEN_CAPTURE"


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

    # legacy / lowercase
    "file_read": FILE_READ,
    "file_delete": FILE_DELETE,
    "terminal": TERMINAL_EXEC,
    "shell": TERMINAL_EXEC,
}


# -------------------------------------------------
# 📌 Registry (ENFORCED SCOPES ONLY)
# -------------------------------------------------

ALL_SCOPES = {
    TERMINAL_EXEC,
    FILE_READ,
    FILE_DELETE,
    SYSTEM_CONTROL,
    NETWORK_CONTROL,
    SCREEN_CAPTURE,
}


# -------------------------------------------------
# 🧩 LEGACY EXPORTS (REQUIRED FOR LOCKED TESTS)
# -------------------------------------------------
# These are aliases ONLY.
# They do NOT expand permission surface.

# Older tests expect APP_CONTROL to exist
APP_CONTROL = SYSTEM_CONTROL
