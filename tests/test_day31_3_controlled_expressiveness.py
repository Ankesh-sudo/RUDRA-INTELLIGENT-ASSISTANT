from core.persona.persona_adapter import PersonaAdapter
from core.persona.persona_contract import PersonaInput


def test_suffix_only_expressiveness():
    text = "Task completed."
    persona_input = PersonaInput(
        text=text,
        tone_hint="playful",
    )

    output, trace = PersonaAdapter.apply(persona_input)

    assert output.startswith(text)
    assert output != text
    assert trace.transformed_text == output


def test_no_rewording_possible():
    text = "System shutting down now."
    persona_input = PersonaInput(text=text)

    output, _ = PersonaAdapter.apply(persona_input)

    assert output == text
