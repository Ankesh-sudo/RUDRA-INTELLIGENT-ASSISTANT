from core.persona.persona_adapter import PersonaAdapter
from core.persona.persona_contract import PersonaInput
from core.persona.persona_toggle import PersonaToggle


def test_persona_disabled_bypasses_adapter():
    PersonaToggle.disable()

    persona_input = PersonaInput(
        text="Operation completed.",
        tone_hint="playful",
    )

    output, trace = PersonaAdapter.apply(persona_input)

    assert output == "Operation completed."
    assert trace is None

    PersonaToggle.enable()


def test_persona_enabled_applies_suffix():
    PersonaToggle.enable()

    persona_input = PersonaInput(
        text="Operation completed.",
        tone_hint="playful",
    )

    output, trace = PersonaAdapter.apply(persona_input)

    assert output.startswith("Operation completed.")
    assert trace is not None
