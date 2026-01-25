class PersonaFreeze:
    """
    One-way persona freeze. Irreversible by design.
    """

    _frozen: bool = False

    @classmethod
    def freeze(cls) -> None:
        cls._frozen = True

    @classmethod
    def is_frozen(cls) -> bool:
        return cls._frozen

    @classmethod
    def assert_frozen(cls) -> None:
        if not cls._frozen:
            raise RuntimeError("Persona maturity not frozen")
