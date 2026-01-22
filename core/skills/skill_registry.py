"""
Skill Registry
Authoritative mapping between Intent and Skill ownership.

Day 50 scope (still valid):
- Ownership only
- No execution
- No permissions
"""

from pyparsing import Enum
from core.nlp.intent import Intent


class Skill(Enum):
    SYSTEM = "system"
    FILESYSTEM = "filesystem"
    NOTES = "notes"
    BASIC = "basic"
    APP = "app"          # Day 60 — App actions


SKILL_REGISTRY = {
    # Day 60 — App control
    Intent.OPEN_APP: Skill.APP,

    # Day 50 — Filesystem
    Intent.LIST_FILES: Skill.FILESYSTEM,

    # Day 50 — Notes
    Intent.NOTE_CREATE: Skill.NOTES,
    Intent.NOTE_READ: Skill.NOTES,
}
