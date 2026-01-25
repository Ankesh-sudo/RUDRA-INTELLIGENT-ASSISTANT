from core.argument.argument_builder import ArgumentBuilder
from core.argument.argument_explain import ArgumentExplain


def test_explain_output():
    builder = ArgumentBuilder()
    chain = builder.build(
        "Water boils at 100°C",
        ["At sea level, water reaches boiling point at 100°C"],
    )

    output = ArgumentExplain.format(chain)
    assert "Claim:" in output
    assert "Premises:" in output
    assert "Conclusion:" in output
