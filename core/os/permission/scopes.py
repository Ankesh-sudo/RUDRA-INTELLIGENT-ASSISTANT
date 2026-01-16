"""
Permission scope definitions.

Rules:
- ALL_SCOPES is the single source of truth
- Canonical scopes are UPPER_SNAKE_CASE
- Aliases may exist for compatibility, but MUST resolve to canonicals
"""

# -------------------------------------------------
# Canonical scopes
# -------------------------------------------------

APP_CONTROL = "APP_CONTROL"
SYSTEM_INFO = "SYSTEM_INFO"
SCREEN_CAPTURE = "SCREEN_CAPTURE"

FILE_READ = "FILE_READ"
FILE_DELETE = "FILE_DELETE"

NETWORK_CONTROL = "NETWORK_CONTROL"


# -------------------------------------------------
# Backward-compat / human aliases (OPTIONAL BUT SAFE)
# -------------------------------------------------
# These are NOT added to ALL_SCOPES directly.
# They exist so higher layers can normalize input if needed.

SCOPE_ALIASES = {
    # file operations
    "filesystem.read": FILE_READ,
    "filesystem.delete": FILE_DELETE,
    "file.read": FILE_READ,
    "file.delete": FILE_DELETE,

    # lowercase variants
    "file_read": FILE_READ,
    "file_delete": FILE_DELETE,
}


# -------------------------------------------------
# Registry
# -------------------------------------------------

ALL_SCOPES = {
    APP_CONTROL,
    SYSTEM_INFO,
    SCREEN_CAPTURE,
    FILE_READ,
    FILE_DELETE,
    NETWORK_CONTROL,
}
