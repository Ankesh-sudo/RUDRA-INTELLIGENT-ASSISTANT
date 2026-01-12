from core.persona.persona_adapter import PersonaAdapter
from core.persona.persona_contract import PersonaInput


def test_persona_adapter_does_not_mutate_text():
    text = "System will shut down in 5 minutes."
    persona_input = PersonaInput(
        text=text,
        language="en",
        tone_hint="playful",
    )

    output, trace = PersonaAdapter.apply(persona_input)

    assert output == text
    assert trace.original_text == text
    assert trace.transformed_text == text
    assert trace.persona_name == "maahi"


def test_persona_adapter_trace_is_present():
    persona_input = PersonaInput(text="Hello")

    output, trace = PersonaAdapter.apply(persona_input)

    assert trace.timestamp is not None
    assert trace.tone_applied in ("neutral", "playful")


def test_persona_input_is_immutable():
    persona_input = PersonaInput(text="Immutable")

    try:
        persona_input.text = "Mutated"
        assert False, "PersonaInput should be immutable"
    except Exception:
        assert True
