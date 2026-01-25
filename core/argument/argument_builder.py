from typing import List
from .claim import Claim
from .premise import Premise
from .conclusion import Conclusion
from .argument_chain import ArgumentChain


class ArgumentBuilder:
    """
    Deterministic argument constructor.
    No inference, no persuasion.
    """

    def build(self, claim_text: str, premise_texts: List[str]) -> ArgumentChain:
        claim = Claim(claim_text)
        claim.validate()

        if not premise_texts:
            raise ValueError("No premises provided")

        premises: List[Premise] = []
        for text in premise_texts:
            premise = Premise(text)
            premise.validate()
            premises.append(premise)

        if len(premises) < 1:
            raise ValueError("Insufficient premises")

        conclusion_text = f"Based on the premises, the claim '{claim.text}' logically follows."
        conclusion = Conclusion(conclusion_text)

        return ArgumentChain(
            claim=claim,
            premises=premises,
            conclusion=conclusion,
        )
