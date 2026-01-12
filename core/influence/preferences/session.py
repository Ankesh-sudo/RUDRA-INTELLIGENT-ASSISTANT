from core.influence.preferences.lifecycle import PreferenceLifecycleError

class PreferenceSession:
    def __init__(self, active_context: str = "session"):
        self.active_context = active_context
        self._previewed = set()
        self._confirmed = set()
        self._applied = {}  # key -> lifetime

    def preview(self, pref):
        self._previewed.add(pref.key)

    def confirm(self, pref):
        if pref.key not in self._previewed:
            raise PreferenceLifecycleError("confirm without preview")
        self._confirmed.add(pref.key)

    def apply(self, pref):
        if pref.key not in self._confirmed:
            raise PreferenceLifecycleError("apply without confirmation")

        # context guard
        if self.active_context not in pref.scope.contexts:
            return False  # safe no-op

        self._applied[pref.key] = pref.scope.lifetime
        return True

    def is_active(self, pref):
        lifetime = self._applied.get(pref.key)
        if lifetime is None:
            return False
        if lifetime == "once":
            return False
        return True
