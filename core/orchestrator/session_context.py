class SessionContext:
    """
    Session-scoped context wrapper.

    Guarantees:
    - No cross-session data leakage
    - No global mutation
    - Thin wrapper over existing working memory
    """

    def __init__(self, working_memory):
        self._memory = working_memory

    def read(self, key, default=None):
        if hasattr(self._memory, "get"):
            return self._memory.get(key, default)
        return default

    def write(self, key, value):
        if hasattr(self._memory, "set"):
            self._memory.set(key, value)

    def has(self, key) -> bool:
        if hasattr(self._memory, "has"):
            return self._memory.has(key)
        return False

    def snapshot(self) -> dict:
        """
        Debug / explain-only snapshot.
        Must NOT expose mutable memory object.
        """
        if hasattr(self._memory, "snapshot"):
            return self._memory.snapshot()
        return {}
