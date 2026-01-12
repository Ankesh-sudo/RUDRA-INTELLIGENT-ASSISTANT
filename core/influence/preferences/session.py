from core.influence.preferences.lifecycle import PreferenceLifecycleError

class PreferenceSession:
    def __init__(self):
        self._previewed = set()
        self._confirmed = set()
        self._applied = set()

    def preview(self, pref):
        self._previewed.add(pref.key)

    def confirm(self, pref):
        if pref.key not in self._previewed:
            raise PreferenceLifecycleError("confirm without preview")
        self._confirmed.add(pref.key)

    def apply(self, pref):
        if pref.key not in self._confirmed:
            raise PreferenceLifecycleError("apply without confirmation")
        self._applied.add(pref.key)
        return True
