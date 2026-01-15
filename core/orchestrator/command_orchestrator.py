"""
Command Orchestrator
Single authoritative gateway for intent execution.

Day 50 scope:
- OPEN_APP only
- No follow-ups
- No retries
"""

from core.skills.skill_registry import SKILL_REGISTRY, Skill
from core.nlp.intent import Intent
from core.skills import system_actions


class CommandOrchestrator:
    def __init__(self, permission_evaluator=None):
        self.permission_evaluator = permission_evaluator

    def execute(self, intent: Intent, args: dict):
        # 1. Resolve skill ownership
        skill = SKILL_REGISTRY.get(intent)

        if not skill:
            return "Intent not implemented."

        # 2. Route to skill
        if skill == Skill.SYSTEM:
            return self._execute_system(intent, args)

        return "Skill not supported yet."

    # ---------------- INTERNAL ----------------

    def _execute_system(self, intent: Intent, args: dict):
        if intent == Intent.OPEN_APP:
            return system_actions.open_app(args)

        return "System intent not supported yet."
