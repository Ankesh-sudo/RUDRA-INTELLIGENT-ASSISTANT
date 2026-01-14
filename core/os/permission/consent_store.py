class ConsentStore:
    """
    In-memory permission store.
    Day 49: no persistence, no I/O.
    """

    def __init__(self):
        self._granted = set()

    def grant(self, scope: str) -> None:
        self._granted.add(scope)

    def revoke(self, scope: str) -> None:
        self._granted.discard(scope)

    def has(self, scope: str) -> bool:
        return scope in self._granted

    def clear_all(self) -> None:
        self._granted.clear()
