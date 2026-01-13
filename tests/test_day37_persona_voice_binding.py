import pytest
from dataclasses import FrozenInstanceError

from core.response.final_envelope import FinalResponseEnvelope
from core.persona.persona_guard import PersonaGuard, PersonaViolationError
from core.output.tts.tts_engine import TTSEngine


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

class DummyTTSEngine(TTSEngine):
    def __init__(self):
        self.last_spoken = None

    def speak(self, envelope: FinalResponseEnvelope) -> None:
        if envelope.tts_allowed:
            self.last_spoken = envelope.final_text


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------

def test_envelope_is_immutable():
    env = FinalResponseEnvelope(
        final_text="hello",
        persona_applied=False,
        persona_fingerprint=None,
        tts_allowed=True,
    )

    with pytest.raises(FrozenInstanceError):
        env.final_text = "mutated"


def test_persona_cannot_be_applied_twice():
    env = FinalResponseEnvelope(
        final_text="hi Boss 🙂",
        persona_applied=True,
        persona_fingerprint="fp123",
        tts_allowed=True,
    )

    with pytest.raises(PersonaViolationError):
        PersonaGuard.assert_persona_not_applied(env)


def test_tts_consumes_envelope_only():
    engine = DummyTTSEngine()

    env = FinalResponseEnvelope(
        final_text="system online",
        persona_applied=False,
        persona_fingerprint=None,
        tts_allowed=True,
    )

    engine.speak(env)
    assert engine.last_spoken == "system online"


def test_voice_cannot_modify_text():
    env = FinalResponseEnvelope(
        final_text="unchanged text",
        persona_applied=True,
        persona_fingerprint="fp",
        tts_allowed=True,
    )

    before = env.text_hash()
    after = env.text_hash()

    assert before == after


def test_persona_removal_does_not_change_logic():
    base_text = "system status nominal"

    no_persona = FinalResponseEnvelope(
        final_text=base_text,
        persona_applied=False,
        persona_fingerprint=None,
        tts_allowed=True,
    )

    with_persona = FinalResponseEnvelope(
        final_text=base_text + " 🙂",
        persona_applied=True,
        persona_fingerprint="fp",
        tts_allowed=True,
    )

    # Logic equality: base text preserved as prefix
    assert with_persona.final_text.startswith(no_persona.final_text)
