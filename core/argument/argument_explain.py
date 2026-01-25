from .argument_chain import ArgumentChain


class ArgumentExplain:
    """
    Formats a human-readable explanation trace.
    """

    @staticmethod
    def format(chain: ArgumentChain) -> str:
        lines = []
        lines.append(f"Claim: {chain.claim.text}")
        lines.append("Premises:")
        for idx, premise in enumerate(chain.premises, start=1):
            lines.append(f"  {idx}. {premise.text}")
        lines.append(f"Conclusion: {chain.conclusion.text}")
        return "\n".join(lines)
