"""
Skill Registry
Authoritative mapping between Intent and Skill ownership.

Day 50 scope:
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


SKILL_REGISTRY = {
    # Day 50 — OS control
    Intent.OPEN_APP: Skill.SYSTEM,

    # (Placeholders for future days; do not wire yet)
    Intent.LIST_FILES: Skill.FILESYSTEM,
    Intent.NOTE_CREATE: Skill.NOTES,
    Intent.NOTE_READ: Skill.NOTES,
}
