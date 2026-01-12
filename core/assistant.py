from loguru import logger

from core.input.input_validator import InputValidator
from core.input_controller import InputController
from core.nlp.normalizer import normalize_text
from core.nlp.intent import Intent
from core.skills.basic import handle as basic_handle
from core.context.short_term import ShortTermContext
from core.context.long_term import save_message
from core.intelligence.intent_scorer import score_intents, pick_best_intent
from core.intelligence.confidence_refiner import refine_confidence
from core.actions.action_executor import ActionExecutor

from core.control.global_interrupt import GLOBAL_INTERRUPT
from core.control.interrupt_words import INTERRUPT_KEYWORDS
from core.control.interrupt_policy import INTERRUPT_POLICY

from core.memory.working_memory import WorkingMemory
from core.memory.context_pack import ContextPackBuilder
from core.memory.follow_up_resolver import FollowUpResolver
from core.memory.slot_preference_merger import SlotPreferenceMerger
from core.memory.confidence_adjuster import ConfidenceAdjuster
from core.memory.memory_manager import MemoryManager
from core.memory.short_term_memory import ShortTermMemory

# 🔵 Day 25.1 — Memory usage mode (DEFAULT OFF)
from core.memory.usage_mode import MemoryUsageMode

# 🔵 Day 25.5 — Memory usage trace sink (session-owned)
from core.memory.trace_sink import MemoryTraceSink

# 🔵 LTM promotion + consent
from core.memory.ltm.promotion_evaluator import (
    MemoryPromotionEvaluator,
    PromotionAction
)

# 🔵 Day 23.2 — Classifier
from core.memory.classifier import MemoryClassifier


INTENT_CONFIDENCE_THRESHOLD = 0.65

CLARIFICATION_MESSAGES = [
    "I’m not sure what you meant. Can you rephrase?",
    "Could you explain that a bit more?",
    "I didn’t fully get that. What would you like to do?",
]

IDLE, ACTIVE, WAITING = "idle", "active", "waiting"

NEGATION_TOKENS = {"dont", "do", "not", "never", "no"}

AFFIRMATIVE = {"yes", "yeah", "yep", "sure", "ok"}
NEGATIVE = {"no", "nope", "nah"}


class Assistant:
    def __init__(self):
        self.input = InputController()
        self.running = True
        self.ctx = ShortTermContext()
        self.input_validator = InputValidator()
        self.state = IDLE

        self.action_executor = ActionExecutor()

        self.pending_intent = None
        self.pending_args = {}
        self.missing_args = []

        self.clarify_index = 0

        self.memory_manager = MemoryManager()
        self.stm = ShortTermMemory()

        # 🔒 Day 25.1 — Memory usage is OFF by default
        self.memory_usage_mode = MemoryUsageMode.DISABLED

        # 🧾 Day 25.5 — Session-owned memory trace sink
        self.memory_trace_sink = MemoryTraceSink()

        # 🔵 Promotion evaluator
        self.memory_promotion_evaluator = MemoryPromotionEvaluator()

        # 🔵 Day 23.2 — Memory classifier
        self.memory_classifier = MemoryClassifier()

    # =================================================
    # UTIL
    # =================================================
    def next_clarification(self):
        msg = CLARIFICATION_MESSAGES[self.clarify_index]
        self.clarify_index = (self.clarify_index + 1) % len(CLARIFICATION_MESSAGES)
        return msg

    def _get_interrupt_policy(self, intent: Intent | None) -> str:
        if not intent:
            return "HARD"
        return INTERRUPT_POLICY.get(intent, "HARD")

    # =================================================
    # EMBEDDED INTERRUPT DETECTION
    # =================================================
    def _detect_embedded_interrupt(self, tokens: list[str]) -> bool:
        for idx, token in enumerate(tokens):
            if token in INTERRUPT_KEYWORDS:
                if idx > 0 and tokens[idx - 1] in NEGATION_TOKENS:
                    return False
                return True
        return False

    # =================================================
    # INTERRUPT HANDLER
    # =================================================
    def _handle_interrupt(self, source: str, intent: Intent | None):
        policy = self._get_interrupt_policy(intent)
        logger.warning(f"Interrupt triggered ({source}) | policy={policy}")

        if policy == "IGNORE":
            return

        if policy == "SOFT":
            print("Rudra > Do you want me to stop this action?")
            return

        GLOBAL_INTERRUPT.trigger()
        self.action_executor.cancel_pending()

        self.pending_intent = None
        self.pending_args = {}
        self.missing_args = []

        self.input.reset_execution_state()
        print("Rudra > Okay, stopped.")
        GLOBAL_INTERRUPT.clear()

    # =================================================
    # CORE SINGLE CYCLE
    # =================================================
    def _cycle(self):
        wm = WorkingMemory()

        context_builder = ContextPackBuilder()
        context_pack = context_builder.build()

        recent_user_stm = self.stm.fetch_recent(
            role="user",
            limit=3,
            min_confidence=0.70
        )
        context_pack["stm_recent"] = recent_user_stm

        follow_up_resolver = FollowUpResolver()
        slot_merger = SlotPreferenceMerger()
        confidence_adjuster = ConfidenceAdjuster()

        raw_text = self.input.read()
        if not raw_text and not self.pending_intent:
            return

        validation = self.input_validator.validate(raw_text)
        if not validation["valid"]:
            print("Rudra > Please repeat.")
            return

        clean_text = validation["clean_text"]
        tokens = normalize_text(clean_text)

        if self._detect_embedded_interrupt(tokens):
            self._handle_interrupt("embedded", self.pending_intent)
            wm.mark_interrupted()
            return

        scores = score_intents(tokens)
        intent, confidence = pick_best_intent(scores, tokens)
        confidence = refine_confidence(
            confidence, tokens, intent.value, self.ctx.last_intent
        )

        wm.set_intent(intent.value, confidence)

        if confidence < INTENT_CONFIDENCE_THRESHOLD or intent == Intent.UNKNOWN:
            resolved = follow_up_resolver.resolve(tokens, context_pack)
            if resolved:
                intent = Intent(resolved["resolved_intent"])
                confidence = 0.7
            else:
                print(self.next_clarification())
                return

        confidence = confidence_adjuster.adjust(
            base_confidence=confidence,
            intent=intent.value,
            context_pack=context_pack
        )

        self.memory_manager.consider(
            role="user",
            content=clean_text,
            intent=intent.value,
            confidence=confidence,
            content_type="conversation"
        )

        save_message("user", clean_text, intent.value)

        if intent == Intent.EXIT:
            print("Rudra > Goodbye!")
            self.running = False
            return

        if intent in (Intent.GREETING, Intent.HELP):
            response = basic_handle(intent, clean_text)
        else:
            result = self.action_executor.execute(intent, clean_text, confidence)
            response = result.get("message", "Done.")

            promotion_plan = self.memory_promotion_evaluator.evaluate(
                confidence=confidence,
                repetition_count=1,
                user_confirmed=False,
                memory_summary=f"{intent.value}: {clean_text}"
            )

            logger.debug(
                f"LTM promotion plan: "
                f"{promotion_plan.action.value} | {promotion_plan.reason}"
            )

            if promotion_plan.action == PromotionAction.ASK_CONSENT:
                print(f"Rudra > {promotion_plan.consent_prompt}")

                reply = (self.input.read() or "").strip().lower()
                user_confirmed = reply in AFFIRMATIVE

                logger.info(f"LTM consent response: confirmed={user_confirmed}")

                if not user_confirmed:
                    print(f"Rudra > Okay, I won’t remember that.")
                    return

                memory_type = self.memory_classifier.classify(clean_text)

                if memory_type is None:
                    print("Rudra > That memory is unclear. I won’t store it.")
                    return

                new_entry = self.memory_manager.store_long_term(
                    content=clean_text,
                    memory_type=memory_type,
                    confidence=confidence,
                    reason="User explicitly approved memory storage"
                )

                conflict = self.memory_manager.detect_conflict(new_entry)

                if conflict:
                    print(
                        f"Rudra > You already told me: '{conflict.content}'. "
                        f"Do you want to replace it with '{new_entry.content}'?"
                    )

                    decision = (self.input.read() or "").strip().lower()

                    if decision in AFFIRMATIVE:
                        self.memory_manager.replace_entry(conflict, new_entry)
                        print("Rudra > Got it. I’ve updated that memory.")
                    else:
                        print("Rudra > Okay, I’ll keep the old one.")

        print(f"Rudra > {response}")
        save_message("assistant", response, intent.value)
        self.ctx.update(intent.value)

    def run(self):
        logger.info("Day 23.4 — Conflict-aware LTM enabled")
        while self.running:
            self._cycle()

    def run_once(self):
        self._cycle()
