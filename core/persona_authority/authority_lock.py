class AuthorityLock:
    """
    Irreversible authority lock.
    Enabled by default and cannot be disabled.
    """

    _locked: bool = True

    @classmethod
    def engage(cls) -> None:
        # Idempotent, irreversible
        cls._locked = True

    @classmethod
    def is_locked(cls) -> bool:
        return cls._locked

    @classmethod
    def assert_locked(cls) -> None:
        if not cls._locked:
            raise RuntimeError("Authority lock is not active")
