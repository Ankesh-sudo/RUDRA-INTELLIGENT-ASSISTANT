class PersonaToggle:
    """
    Central switch for persona layer.
    Fail-closed by design.
    """

    _enabled: bool = True

    @classmethod
    def enable(cls) -> None:
        cls._enabled = True

    @classmethod
    def disable(cls) -> None:
        cls._enabled = False

    @classmethod
    def is_enabled(cls) -> bool:
        return cls._enabled
