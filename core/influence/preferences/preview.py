class PreferencePreview:
    """
    Presentation-only preview of a preference.
    Must not imply behavior beyond wording/tone.
    """
    def __init__(self, preference, preview_text: str):
        self.preference = preference
        self.preview_text = preview_text

    def is_consistent(self) -> bool:
        # Hard guard: preference key must be tone/language-only
        if not isinstance(self.preview_text, str):
            return False

        key_ok = self.preference.key.startswith("tone.")
        text_ok = not any(
            word in self.preview_text.lower()
            for word in ["execute", "command", "logic", "memory", "decision"]
        )
        return key_ok and text_ok
