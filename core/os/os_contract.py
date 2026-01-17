"""
OS CONTRACT
Day 50 — SEALED

This file defines the ONLY valid OS action categories and action types.
Anything not declared here MUST be rejected.

NO dynamic categories
NO inferred actions
NO shortcuts
"""

from typing import Dict, Set


# ==========================================================
# VALID ACTION CATEGORIES (STRICT)
# ==========================================================
# These MUST match linux backends under core/os/linux/
# ----------------------------------------------------------

CATEGORY_APP = "app"
CATEGORY_SYSTEM = "system"
CATEGORY_FILE = "file"

VALID_CATEGORIES: Set[str] = {
    CATEGORY_APP,
    CATEGORY_SYSTEM,
    CATEGORY_FILE,
}


# ==========================================================
# ACTION TYPES PER CATEGORY (STRICT)
# ==========================================================

ACTIONS_BY_CATEGORY: Dict[str, Set[str]] = {

    # ------------------------------------------------------
    # APPLICATION CONTROL
    # core/os/linux/app_control.py
    # ------------------------------------------------------
    CATEGORY_APP: {
        "OPEN_APP",
        "CLOSE_APP",
        "FOCUS_APP",
    },

    # ------------------------------------------------------
    # SYSTEM INFORMATION / CONTROL
    # core/os/linux/system_info.py
    # ------------------------------------------------------
    CATEGORY_SYSTEM: {
        "SYSTEM_INFO",
        "SCREENSHOT",
    },

    # ------------------------------------------------------
    # FILE OPERATIONS
    # core/os/file_ops/file_executor.py
    # ------------------------------------------------------
    CATEGORY_FILE: {
        "OPEN_FILE",
        "LIST_FILES",
        "DELETE_FILE",
    },
}


# ==========================================================
# CONTRACT VALIDATORS
# ==========================================================

def validate_category(category: str) -> None:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")


def validate_action(category: str, action_type: str) -> None:
    validate_category(category)

    allowed = ACTIONS_BY_CATEGORY.get(category, set())
    if action_type not in allowed:
        raise ValueError(
            f"Invalid action '{action_type}' for category '{category}'"
        )


# ==========================================================
# CONTRACT HELPERS
# ==========================================================

def is_valid(category: str, action_type: str) -> bool:
    try:
        validate_action(category, action_type)
        return True
    except ValueError:
        return False
