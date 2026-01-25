# core/terminal/confirm_gate.py

class ConfirmationGate:
    """
    Explicit YES-only confirmation gate.
    Any other input aborts.
    """

    CONFIRM_WORD = "YES"

    @staticmethod
    def confirm(user_input: str) -> bool:
        return user_input.strip() == ConfirmationGate.CONFIRM_WORD
