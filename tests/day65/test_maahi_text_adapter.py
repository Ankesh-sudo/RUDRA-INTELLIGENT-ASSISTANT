import pytest

from core.response.final_envelope import FinalResponseEnvelope
from core.response.phrasing_adapter import MaahiTextAdapter


def make_envelope(
    *,
    text: str = "Opening Chrome",
    persona_applied: bool = False,
    persona_hint: str | None = None,
):
    return FinalResponseEnvelope(
        final_text=text,
        persona_applied=persona_applied,
        persona_hint=persona_hint,
        persona_fingerprint="maahi_v1",
        tts_allowed=True,
    )


def test_persona_disabled_passthrough():
    envelope = make_envelope(
        persona_applied=False,
        persona_hint="CONFIRM_ACTION",
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == envelope.final_text


def test_persona_enabled_with_hint_applies_phrase():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint="CONFIRM_ACTION",
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == "Got it, Boss. Doing it now."


def test_persona_enabled_without_hint_passthrough():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint=None,
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == envelope.final_text


def test_unknown_hint_passthrough():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint="UNKNOWN_HINT",
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == envelope.final_text


def test_action_complete_phrase():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint="ACTION_COMPLETE",
        text="Chrome opened",
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == "All set, Boss."


def test_action_failed_phrase():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint="ACTION_FAILED",
        text="Failed to open Chrome",
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == "Sorry Boss, that didn’t work."


def test_cancelled_phrase():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint="CANCELLED",
        text="Action cancelled",
    )

    result = MaahiTextAdapter.apply(envelope)

    assert result == "Okay Boss, I’ve cancelled it."


def test_canonical_text_hash_unchanged():
    envelope = make_envelope(
        persona_applied=True,
        persona_hint="CONFIRM_ACTION",
    )

    original_hash = envelope.text_hash()
    _ = MaahiTextAdapter.apply(envelope)

    assert envelope.text_hash() == original_hash
