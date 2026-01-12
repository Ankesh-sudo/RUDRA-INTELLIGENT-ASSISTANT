from typing import List

from core.memory.influence.contract import MemoryInfluenceContract
from core.memory.influence.signal import InfluenceSignal


class NoOpMemoryInfluence(MemoryInfluenceContract):
    """
    Safe default. Evaluates influence but applies nothing.
    """

    def evaluate(
        self,
        *,
        recalled_memories: list,
        permit,
        usage_mode: str,
        context: dict,
    ) -> List[InfluenceSignal]:
        return []
