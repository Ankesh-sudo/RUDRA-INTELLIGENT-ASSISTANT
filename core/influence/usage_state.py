from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PreferenceUsageState:
    enabled: bool
    expires_at_session: Optional[str]
    reason: str

    @staticmethod
    def disabled(reason: str) -> "PreferenceUsageState":
        return PreferenceUsageState(
            enabled=False,
            expires_at_session=None,
            reason=reason,
        )

    @staticmethod
    def enabled_for_session(session_id: str) -> "PreferenceUsageState":
        return PreferenceUsageState(
            enabled=True,
            expires_at_session=session_id,
            reason="enabled for session",
        )

    def is_expired(self, current_session_id: str) -> bool:
        if not self.enabled:
            return True
        if self.expires_at_session is None:
            return True
        return self.expires_at_session != current_session_id
