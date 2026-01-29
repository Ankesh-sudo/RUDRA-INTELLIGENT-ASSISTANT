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
from core.explain.formatter import ExplainFormatter  # ✅ STEP 6

# 🧠 Response Envelope (STEP 5)
from core.response.final_envelope import FinalResponseEnvelope

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


# =================================================
# STATIC RESPONSES
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

        # Knowledge (read-only)
        try:
            self.knowledge = build_knowledge_engine()
        except Exception:
            logger.exception("Failed to bootstrap Knowledge Engine")
            self.knowledge = None

        engine_key = PERSONA_VOICE_MAP.get("maahi")
        self.tts_engine = TTSEngineRegistry.get(engine_key) if engine_key else None

        # STEP 6 — last explain surface (read-only)
        self._last_explain: ExplainSurface | None = None

    # =================================================
    # SINGLE RESPONSE GATE — STEP 5 (LOCKED)
    # =================================================
    def respond(
        self,
        *,
        text: str,
        explain: ExplainSurface | None = None,
    ) -> FinalResponseEnvelope:
        """
        Authoritative output gate.
        ExplainSurface is stored, not embedded.
        """
        envelope = FinalResponseEnvelope(
            final_text=text,
            persona_applied=False,
            persona_hint=None,
            persona_fingerprint=None,
            tts_allowed=True,
        )

        # STEP 6 — store explain surface
        self._last_explain = explain

        # CLI output
        print(f"Rudra > {envelope.final_text}")

        return envelope

    # =================================================
    # NON-EXECUTION HANDLERS
    # =================================================
    def handle_help(self):
        return self.respond(
            text=HELP_TEXT,
            explain=ExplainSurface.single(HELP_TEXT),
        )

    def handle_capabilities(self):
        return self.respond(
            text=CAPABILITIES_TEXT,
            explain=ExplainSurface.single(CAPABILITIES_TEXT),
        )

    def handle_identity(self):
        return self.respond(
            text=IDENTITY_TEXT,
            explain=ExplainSurface.single(IDENTITY_TEXT),
        )

    # =================================================
    # KNOWLEDGE — DHARMA
    # =================================================
    def handle_dharma(self):
        if not self.knowledge:
            return self.respond(
                text="Knowledge system is not available right now.",
                explain=ExplainSurface.single(
                    "Knowledge engine unavailable."
                ),
            )

        payload = self.knowledge.query("dharma")

        if not payload:
            return self.respond(
                text="I don't have enough information about dharma yet.",
                explain=ExplainSurface.single(
                    "No matching knowledge entry found."
                ),
            )

        if isinstance(payload, str):
            return self.respond(
                text=payload,
                explain=ExplainSurface.single(payload),
            )

        return self.respond(
            text=payload.get("answer", ""),
            explain=ExplainSurface.from_knowledge(payload),
        )

    # =================================================
    # CORE LOOP
    # =================================================
    def _cycle(self):
        raw_text = self.input.read()
        if not raw_text:
            return

        validation = self.input_validator.validate(raw_text)
        if not validation["valid"]:
            self.respond(
                text="Please repeat.",
                explain=ExplainSurface.single("Input validation failed."),
            )
            return

        clean_text = validation["clean_text"]
        lowered = clean_text.lower().strip()

        # =================================================
        # STEP 6 — EXPLAIN TOGGLE (META COMMAND)
        # =================================================
        if validation.get("is_explain_request"):
            if not self._last_explain:
                return self.respond(
                    text="There is no previous decision to explain.",
                    explain=None,
                )

            formatted = ExplainFormatter.format_for_user(self._last_explain)
            return self.respond(
                text=formatted,
                explain=self._last_explain,
            )

        # -------------------------------------------------
        # STATIC COMMANDS
        # -------------------------------------------------
        if lowered in {"help", "commands"}:
            return self.handle_help()

        if lowered in {"what can you do", "capabilities"}:
            return self.handle_capabilities()

        if lowered in {"who are you", "what are you"}:
            return self.handle_identity()

        if lowered in {
            "what is dharma",
            "define dharma",
            "explain dharma",
            "tell me about dharma",
        }:
            return self.handle_dharma()

        # -------------------------------------------------
        # INTENT ROUTING
        # -------------------------------------------------
        tokens = normalize_text(clean_text)
        scores = score_intents(tokens)
        intent, confidence = pick_best_intent(scores, tokens)
        confidence = refine_confidence(
            confidence, tokens, intent.value, self.ctx.last_intent
        )

        if confidence < INTENT_CONFIDENCE_THRESHOLD:
            return self.respond(
                text="I’m not sure what you meant.",
                explain=ExplainSurface.single(
                    "Intent confidence below threshold."
                ),
            )

        save_message("user", clean_text, intent.value)

        if intent == Intent.EXIT:
            self.respond(
                text="Goodbye!",
                explain=ExplainSurface.single("Session ended."),
            )
            self.running = False
            return

        result = self.action_executor.execute(intent, clean_text, confidence)
        message = result.get("message", "Done.")

        self.respond(
            text=message,
            explain=ExplainSurface.from_action(message),
        )

        save_message("assistant", message, intent.value)

    def run(self):
        logger.info("Day 40 — Persona & Voice frozen")
        while self.running:
            self._cycle()
