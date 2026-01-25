from enum import Enum, auto


class DialogueIntent(Enum):
    """
    High-level dialogue meanings.
    NOT commands.
    NOT actions.
    NOT memory triggers.
    """

    SMALL_TALK = auto()
    EMOTIONAL_CHECK = auto()
    ACKNOWLEDGEMENT = auto()
    CLARIFICATION = auto()
    UNKNOWN = auto()


class DialogueResponseStyle(Enum):
    """
    Response planning hints.
    DOES NOT control persona tone or voice.
    """

    NEUTRAL = auto()
    POLITE = auto()
    BRIEF = auto()


class DialogueSafety(Enum):
    """
    Safety classification for dialogue turns.
    Used later (Day 72+) for enforcement checks.
    """

    SAFE = auto()
    REQUIRES_GUARD = auto()
    BLOCKED = auto()
