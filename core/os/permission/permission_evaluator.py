from dataclasses import dataclass
from typing import Optional, Set

from core.os.permission.consent_store import ConsentStore
from core.os.permission.consent_prompt import ConsentPrompt


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    requires_confirmation: bool
    missing_scopes: Set[str]
    prompt_payload: Optional[dict]


class PermissionEvaluator:
    """
    Central authority for permission decisions.
    Persona has ZERO access here.
    """

    def __init__(self, consent_store: ConsentStore):
        self._store = consent_store

    def evaluate(self, action_spec) -> PermissionDecision:
        missing = {
            scope
            for scope in action_spec.required_scopes
            if not self._store.has(scope)
        }

        if missing:
            return PermissionDecision(
                allowed=False,
                requires_confirmation=True,
                missing_scopes=missing,
                prompt_payload=ConsentPrompt.build(action_spec, missing),
            )

        if action_spec.requires_confirmation:
            return PermissionDecision(
                allowed=True,
                requires_confirmation=True,
                missing_scopes=set(),
                prompt_payload=ConsentPrompt.build(action_spec, set()),
            )

        return PermissionDecision(
            allowed=True,
            requires_confirmation=False,
            missing_scopes=set(),
            prompt_payload=None,
        )
