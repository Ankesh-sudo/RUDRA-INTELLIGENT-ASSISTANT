import re
from typing import List

from core.response.final_envelope import FinalResponseEnvelope


class PersonaViolationError(RuntimeError):
    """
    Raised when persona invariants are violated.
    """
    pass


class PersonaGuard:
    """
    Enforces persona safety invariants.

    Design principles:
    - Conservative: reject rather than alter
    - Meaning-preserving
    - Suffix-only expressiveness
    - Single-use persona application (Day 37)
    """

    # ------------------------------------------------------------------
    # Internal helpers (unchanged from Day 31)
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(text: str) -> List[str]:
        """
        Normalize text for strict semantic comparison.
        """
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text.split()

    # ------------------------------------------------------------------
    # Semantic safety (Day 31.2 — unchanged)
    # ------------------------------------------------------------------

    @classmethod
    def is_semantically_safe(cls, original: str, transformed: str) -> bool:
        """
        Semantic safety rule:

        - Same word sequence
        - Same length
        - Same order

        NOTE:
        This validates the semantic *core* only.
        It does NOT allow suffix expressiveness.
        """
        if original == transformed:
            return True

        o = cls._normalize(original)
        t = cls._normalize(transformed)

        if len(o) != len(t):
            return False

        return o == t

    # ------------------------------------------------------------------
    # Prefix preservation (Day 31.3 — unchanged)
    # ------------------------------------------------------------------

    @classmethod
    def is_prefix_preserved(cls, original: str, transformed: str) -> bool:
        """
        Persona output MUST preserve original text as a prefix.

        This allows suffix-only expressiveness
        (emoji / warmth)
        while forbidding:
        - rewording
        - insertion
        - deletion
        """
        return transformed.startswith(original)

    # ------------------------------------------------------------------
    # Day 37 — NEW HARD LOCKS
    # ------------------------------------------------------------------

    @staticmethod
    def assert_persona_not_applied(envelope: FinalResponseEnvelope) -> None:
        """
        Day 37 invariant:

        Persona may be applied EXACTLY ONCE.

        Any attempt to apply persona when an envelope already
        indicates persona_applied=True is a hard violation.
        """
        if envelope.persona_applied:
            raise PersonaViolationError(
                "Persona already applied; reapplication forbidden"
            )

    @staticmethod
    def assert_envelope_integrity(envelope: FinalResponseEnvelope) -> None:
        """
        Day 37 invariant:

        Persona guard operates ONLY on FinalResponseEnvelope,
        never on raw strings.

        This ensures:
        - single source of truth
        - correct layering
        """
        if not isinstance(envelope, FinalResponseEnvelope):
            raise PersonaViolationError(
                "PersonaGuard requires FinalResponseEnvelope"
            )

    # ------------------------------------------------------------------
    # Composite validation (used by PersonaApplier)
    # ------------------------------------------------------------------

    @classmethod
    def validate_persona_application(
        cls,
        original_text: str,
        transformed_text: str,
        prior_envelope: FinalResponseEnvelope | None = None,
    ) -> None:
        """
        Full persona validation entry point.

        Enforces:
        - single-use persona
        - semantic safety
        - prefix preservation
        """

        if prior_envelope is not None:
            cls.assert_envelope_integrity(prior_envelope)
            cls.assert_persona_not_applied(prior_envelope)

        if not cls.is_prefix_preserved(original_text, transformed_text):
            raise PersonaViolationError(
                "Persona output must preserve original text as prefix"
            )

        # Semantic core must match
        if not cls.is_semantically_safe(
            original_text,
            transformed_text[: len(original_text)],
        ):
            raise PersonaViolationError(
                "Persona altered semantic core"
            )
