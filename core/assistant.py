from loguru import logger

from core.input.input_validator import InputValidator
from core.input_controller import InputController
from core.nlp.normalizer import normalize_text
from core.nlp.intent import Intent
from core.context.short_term import ShortTermContext
from core.context.long_term import save_message
from core.intelligence.intent_scorer import score_intents, pick_best_intent
from core.intelligence.confidence_refiner import refine_confidence
from core.actions.action_executor import ActionExecutor

# 🧠 Explain Surface (STEP 4)
from core.explain.explain_surface import ExplainSurface

# 🧠 Knowledge bootstrap
from core.knowledge.bootstrap import build_knowledge_engine

# 🔵 Memory
from core.memory.short_term_memory import ShortTermMemory
from core.memory.usage_mode import MemoryUsageMode
from core.memory.trace_sink import MemoryTraceSink
from core.memory.ltm.promotion_evaluator import MemoryPromotionEvaluator
from core.memory.classifier import MemoryClassifier
from core.memory.memory_manager import MemoryManager

# 🔊 TTS (still disabled)
from core.output.tts.tts_registry import TTSEngineRegistry
from core.output.tts.voice_routing import PERSONA_VOICE_MAP

# 🔐 Permissions
from core.os.permission.consent_store import ConsentStore
from core.os.permission.permission_registry import PermissionRegistry


# =================================================
# STEP 2 — STATIC NON-EXECUTION RESPONSES
# =================================================
HELP_TEXT = (
    "I can help with system actions, notes, and basic queries.\n"
    "Try commands like:\n"
    "- help\n"
    "- what can you do\n"
    "- who are you\n"
    "- what is dharma\n"
    "- exit"
)

CAPABILITIES_TEXT = (
    "My current capabilities include:\n"
    "- Opening applications\n"
    "- Opening websites (safe & whitelisted)\n"
    "- Taking simple notes\n"
    "- Safe terminal previews\n"
    "- Answering knowledge questions (Dharma)"
)

IDENTITY_TEXT = (
    "I am Rudra — a deterministic, safety-first assistant.\n"
    "I execute actions reliably and explain what I do."
)

INTENT_CONFIDENCE_THRESHOLD = 0.65


class Assistant:
    def __init__(self):
        self.input = InputController()
        self.running = True
        self.ctx = ShortTermContext()
        self.input_validator = InputValidator()

        self.action_executor = ActionExecutor()

        self.memory_manager = MemoryManager()
        self.stm = ShortTermMemory()
        self.memory_usage_mode = MemoryUsageMode.DISABLED
        self.memory_trace_sink = MemoryTraceSink()
        self.memory_promotion_evaluator = MemoryPromotionEvaluator()
        self.memory_classifier = MemoryClassifier()

        # 🧠 Knowledge Engine (READ-ONLY, BOOTSTRAPPED ONCE)
        try:
            self.knowledge = build_knowledge_engine()
        except Exception:
            logger.exception("Failed to bootstrap Knowledge Engine")
            self.knowledge = None

        engine_key = PERSONA_VOICE_MAP.get("maahi")
        self.tts_engine = TTSEngineRegistry.get(engine_key) if engine_key else None

        self.consent_store = ConsentStore()
        self.clarify_index = 0

    # =================================================
    # SINGLE RESPONSE GATE (STEP 1)
    # =================================================
    def respond(self, surface: ExplainSurface | str) -> str:
        """
        Single authoritative output gate.
        Step 4 allows ExplainSurface OR raw string.
        """
        if isinstance(surface, ExplainSurface):
            text = surface.as_text()
        else:
            text = str(surface)

        print(f"Rudra > {text}")
        return text

    # =================================================
    # STEP 2 — NON-EXECUTION HANDLERS
    # =================================================
    def handle_help(self):
        return self.respond(ExplainSurface.single(HELP_TEXT))

    def handle_capabilities(self):
        return self.respond(ExplainSurface.single(CAPABILITIES_TEXT))

    def handle_identity(self):
        return self.respond(ExplainSurface.single(IDENTITY_TEXT))

    # =================================================
    # STEP 3 — KNOWLEDGE HANDLER (DHARMA)
    # =================================================
    def handle_dharma(self):
        if not self.knowledge:
            return self.respond(
                ExplainSurface.single(
                    "Knowledge system is not available right now."
                )
            )

        try:
            payload = self.knowledge.query("dharma")
        except Exception:
            logger.exception("Knowledge engine error")
            return self.respond(
                ExplainSurface.single(
                    "I couldn't retrieve knowledge about dharma right now."
                )
            )

        if not payload:
            return self.respond(
                ExplainSurface.single(
                    "I don't have enough information about dharma yet."
                )
            )

        surface = ExplainSurface.from_knowledge(payload)
        return self.respond(surface)

    # =================================================
    # CORE LOOP
    # =================================================
    def _cycle(self):
        raw_text = self.input.read()
        if not raw_text:
            return

        validation = self.input_validator.validate(raw_text)
        if not validation["valid"]:
            self.respond(ExplainSurface.single("Please repeat."))
            return

        clean_text = validation["clean_text"]
        lowered = clean_text.lower().strip()

        # STEP 2 — UI COMMANDS
        if lowered in {"help", "commands"}:
            return self.handle_help()

        if lowered in {"what can you do", "capabilities"}:
            return self.handle_capabilities()

        if lowered in {"who are you", "what are you"}:
            return self.handle_identity()

        # STEP 3 — KNOWLEDGE
        if lowered in {
            "what is dharma",
            "define dharma",
            "explain dharma",
            "tell me about dharma",
        }:
            return self.handle_dharma()

        # EXECUTION PATH (UNCHANGED)
        tokens = normalize_text(clean_text)
        scores = score_intents(tokens)
        intent, confidence = pick_best_intent(scores, tokens)
        confidence = refine_confidence(
            confidence, tokens, intent.value, self.ctx.last_intent
        )

        if confidence < INTENT_CONFIDENCE_THRESHOLD:
            return self.respond(
                ExplainSurface.single("I’m not sure what you meant.")
            )

        save_message("user", clean_text, intent.value)

        if intent == Intent.EXIT:
            self.respond(ExplainSurface.single("Goodbye!"))
            self.running = False
            return

        result = self.action_executor.execute(intent, clean_text, confidence)
        response = result.get("message", "Done.")

        surface = ExplainSurface.from_action(response)
        self.respond(surface)

        save_message("assistant", response, intent.value)

    def run(self):
        logger.info("Day 40 — Persona & Voice frozen")
        while self.running:
            self._cycle()
