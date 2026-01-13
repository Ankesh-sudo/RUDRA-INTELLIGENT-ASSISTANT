# tests/test_day36_2_persona_no_memory_access.py

import inspect
import sys

# Persona modules to inspect
PERSONA_MODULES = [
    "core.persona.persona_adapter",
    "core.persona.conversational_style_adapter",
]

# Forbidden imports
FORBIDDEN_PREFIXES = (
    "core.memory",
    "core.stm",
    "core.ltm",
    "core.influence",
    "core.preferences",
    "core.context",
    "core.intent",
)


def test_persona_modules_do_not_import_memory():
    for module_name in PERSONA_MODULES:
        module = __import__(module_name, fromlist=["*"])
        source = inspect.getsource(module)

        for forbidden in FORBIDDEN_PREFIXES:
            assert forbidden not in source, (
                f"Persona module '{module_name}' illegally imports '{forbidden}'"
            )
