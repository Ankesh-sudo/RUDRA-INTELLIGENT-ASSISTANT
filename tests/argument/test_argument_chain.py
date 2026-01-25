from core.argument.claim import Claim
from core.argument.premise import Premise
from core.argument.conclusion import Conclusion
from core.argument.argument_chain import ArgumentChain


def test_argument_chain_creation():
    claim = Claim("Water boils at 100°C")
    premises = [Premise("At sea level, water reaches boiling point at 100°C")]
    conclusion = Conclusion("Therefore, water boils at 100°C")

    chain = ArgumentChain(claim, premises, conclusion)
    assert chain.claim.text == "Water boils at 100°C"
