from typing import Dict


EXPLAIN_COMMANDS = {
    "explain",
    "why",
    "how did you decide",
}


class InputValidator:
    def __init__(self):
        self._last_input = None
        self._last_result = None  # "accepted" or "rejected"

    def mark_rejected(self):
        self._last_result = "rejected"

    def _is_explain_request(self, text: str) -> bool:
        return text in EXPLAIN_COMMANDS

    def validate(self, raw_text: str) -> Dict[str, str | bool]:
        if not raw_text:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": "",
                "reason": "empty",
                "is_explain_request": False,
            }

        # Basic string cleanup ONLY (no NLP here)
        clean_text = raw_text.strip().lower()

        if not clean_text:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": "",
                "reason": "empty",
                "is_explain_request": False,
            }

        is_explain_request = self._is_explain_request(clean_text)

        # Too short (characters) — EXCEPT explain commands
        if not is_explain_request and len(clean_text) < 3:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": clean_text,
                "reason": "too_short",
                "is_explain_request": False,
            }

        words = clean_text.split()

        # Too few words — EXCEPT explain commands
        if not is_explain_request and len(words) < 1:
            self._last_result = "rejected"
            return {
                "valid": False,
                "clean_text": clean_text,
                "reason": "too_few_words",
                "is_explain_request": False,
            }

        # Repeat suppression ONLY if last input was accepted
        # Explain commands are allowed to repeat
        if (
            not is_explain_request
            and self._last_input
            and clean_text == self._last_input
            and self._last_result == "accepted"
        ):
            return {
                "valid": False,
                "clean_text": clean_text,
                "reason": "repeat",
                "is_explain_request": False,
            }

        # Accept input
        self._last_input = clean_text
        self._last_result = "accepted"

        return {
            "valid": True,
            "clean_text": clean_text,
            "reason": None,
            "is_explain_request": is_explain_request,
        }
