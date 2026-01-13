from typing import Optional


class PersonaExpressiveness:
    """
    Whitelisted, suffix-only expressiveness.
    Zero semantic power.
    """

    SAFE_SUFFIXES = {
        "neutral": "",
        "warm": " 🙂",
        "playful": " 😊",
        "affectionate": " 💖",
    }

    @classmethod
    def apply_suffix(cls, text: str, tone: Optional[str]) -> str:
        suffix = cls.SAFE_SUFFIXES.get(tone or "neutral", "")
        return text + suffix
