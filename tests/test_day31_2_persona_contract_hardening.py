from core.persona.persona_guard import PersonaGuard
from core.persona.persona_adapter import PersonaAdapter
from core.persona.persona_contract import PersonaInput


def test_guard_accepts_identical_text():
    text = "System will shut down in 5 minutes"
    assert PersonaGuard.is_semantically_safe(text, text)


def test_guard_rejects_rewording():
    original = "System will shut down in 5 minutes"
    transformed = "The system will shut down in five minutes"

    assert not PersonaGuard.is_semantically_safe(original, transformed)


def test_adapter_fallback_on_violation():
    persona_input = PersonaInput(
        text="System update completed",
        tone_hint="playful",
    )

    output, trace = PersonaAdapter.apply(persona_input)

    assert output == persona_input.text
    assert trace.transformed_text == persona_input.text
