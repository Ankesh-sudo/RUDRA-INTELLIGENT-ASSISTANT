from .counter_chain import CounterChain


class CounterExplain:
    """
    Formats a readable counter-argument explanation.
    """

    @staticmethod
    def format(chain: CounterChain) -> str:
        lines = []
        lines.append(f"Original Claim: {chain.argument.claim.text}")

        if chain.is_empty():
            lines.append("No strong counter-argument found.")
            return "\n".join(lines)

        lines.append("Counter Points:")
        for idx, counter in enumerate(chain.counters, start=1):
            lines.append(f"  {idx}. ({counter.strategy}) {counter.description}")

        return "\n".join(lines)
