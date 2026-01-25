from typing import List
from .claim import Claim
from .premise import Premise
from .conclusion import Conclusion


class ArgumentChain:
    """
    Linear, non-branching argument structure.
    """

    def __init__(self, claim: Claim, premises: List[Premise], conclusion: Conclusion):
        if not premises:
            raise ValueError("Argument requires at least one premise")

        self.claim = claim
        self.premises = premises
        self.conclusion = conclusion

    def explain(self) -> dict:
        return {
            "claim": self.claim.text,
            "premises": [p.text for p in self.premises],
            "conclusion": self.conclusion.text,
        }
