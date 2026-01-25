import pytest
from core.argument.argument_builder import ArgumentBuilder


def test_abort_without_premises():
    builder = ArgumentBuilder()
    with pytest.raises(ValueError):
        builder.build("The sky is blue", [])
