# core/runtime/brain.py

from pathlib import Path

from core.response.final_envelope import FinalResponseEnvelope
from core.os.executor.guarded_executor import GuardedExecutor
from core.knowledge.engine import KnowledgeEngine
from core.knowledge.loader import load_dharma_csv
from core.nlp.intent import Intent
from core.os.action_spec import ActionSpec
from core.actions.planned_action import PlannedAction


class Brain:
    """
    Single authoritative decision-maker.

    NOTE (IMPORTANT):
    - NLP uses Enum-based Intent
    - ActionPlanner expects class-based intents
    - For now, Brain performs direct intent→action mapping
    """

    def __init__(self):
        # ── Knowledge wiring
        root_dir = Path(__file__).resolve().parents[2]
        data_dir = root_dir / "data" / "dharma"

        rows = []
        rows.extend(load_dharma_csv(data_dir / "dharma_base.csv"))
        rows.extend(load_dharma_csv(data_dir / "gita.csv"))
        rows.extend(load_dharma_csv(data_dir / "upanishads.csv"))
        rows.extend(load_dharma_csv(data_dir / "yoga_sutras.csv"))

        self.knowledge = KnowledgeEngine(rows)
        self.executor = GuardedExecutor()

        # ── Direct intent → action mapping (Enum-based, correct for now)
        self.intent_to_action = {
            Intent.OPEN_APP: "OPEN_APP",
            Intent.OPEN_TERMINAL: "OPEN_TERMINAL",
            Intent.OPEN_BROWSER: "OPEN_BROWSER",
            Intent.LIST_FILES: "LIST_FILES",
        }

    def process(self, intent, context=None) -> FinalResponseEnvelope:
        # 1️⃣ KNOWLEDGE
        if intent == Intent.HELP:
            return self._handle_help()

        if intent.name == "WHAT_IS_DHARMA":
            return self._handle_knowledge(intent)

        # 2️⃣ ACTIONS
        if intent in self.intent_to_action:
            action_type = self.intent_to_action[intent]

            action_spec = ActionSpec(
                action_type=action_type,
                category="SYSTEM",
                target=None,
                parameters={},
                risk_level="LOW",
                required_scopes=set(),
                destructive=False,
                supports_undo=False,
                requires_preview=False,
            )

            planned = PlannedAction(
                action_spec=action_spec,
                source_intent=intent,
            )

            result = self.executor.execute([planned])

            return FinalResponseEnvelope(
                final_text=result.summary,
                persona_applied=False,
                tts_allowed=True,
            )

        # 3️⃣ FALLBACK
        return FinalResponseEnvelope(
            final_text="I understood your words, but I don’t know how to act on this yet.",
            persona_applied=False,
            tts_allowed=False,
        )

    def _handle_knowledge(self, intent) -> FinalResponseEnvelope:
        answer = self.knowledge.query(intent.value)
        return FinalResponseEnvelope(
            final_text=answer,
            persona_applied=False,
            tts_allowed=True,
        )

    def _handle_help(self) -> FinalResponseEnvelope:
        return FinalResponseEnvelope(
            final_text=(
                "I can open applications, open the terminal or browser, "
                "list files, and answer questions about Dharma."
            ),
            persona_applied=False,
            tts_allowed=True,
        )
