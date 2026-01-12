from typing import Iterable, List, Set

from core.influence.preference_preview import PreferencePreview


class PreferenceConfirmation:
    """
    Session-local confirmation gate.
    Default: nothing confirmed.
    """

    def __init__(self) -> None:
        self._confirmed: Set[str] = set()
        self._rejected: Set[str] = set()

    def preview(self, previews: List[PreferencePreview]) -> List[PreferencePreview]:
        return previews

    def confirm(self, keys: Iterable[str]) -> None:
        for k in keys:
            self._confirmed.add(k)
            self._rejected.discard(k)

    def reject(self, keys: Iterable[str]) -> None:
        for k in keys:
            self._rejected.add(k)
            self._confirmed.discard(k)

    def confirmed_keys(self) -> Set[str]:
        return set(self._confirmed)

    def clear(self) -> None:
        self._confirmed.clear()
        self._rejected.clear()
