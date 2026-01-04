from typing import Dict


class InputValidator:
    def __init__(self):
        self._last_input = None
        self._last_result = None  # "accepted" or "rejected"

    def mark_rejected(self):
        self._last_result = "rejected"

    def validate(self, raw_text: str) -> Dict[str, str | bool]:
        if not raw_text:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": "",
                "reason": "empty"
            }

        # Basic string cleanup ONLY (no NLP here)
        clean_text = raw_text.strip().lower()

        if not clean_text:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": "",
                "reason": "empty"
            }

        # Too short (characters)
        if len(clean_text) < 3:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": clean_text,
                "reason": "too_short"
            }

        words = clean_text.split()

        # Too few words
        if len(words) < 1:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": clean_text,
                "reason": "too_few_words"
            }

        # Repeat suppression ONLY if last input was accepted
        if (
            self._last_input
            and clean_text == self._last_input
            and self._last_result == "accepted"
        ):
            return {
                "valid": False,
                "clean_text": clean_text,
                "reason": "repeat"
            }

        # Accept input
        self._last_input = clean_text
        self._last_result = "accepted"

        return {
            "valid": True,
            "clean_text": clean_text,
            "reason": None
        }
