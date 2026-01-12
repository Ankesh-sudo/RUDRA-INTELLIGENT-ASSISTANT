from abc import ABC, abstractmethod
from typing import List

from core.memory.influence.signal import InfluenceSignal


class MemoryInfluenceContract(ABC):
    """
    Advisory-only influence interface.
    Implementations MUST be deterministic and side-effect free.
    """

    @abstractmethod
    def evaluate(
        self,
        *,
        recalled_memories: list,
        permit,
        usage_mode: str,
        context: dict,
    ) -> List[InfluenceSignal]:
        """
        Returns a list of InfluenceSignal.
        Returning an empty list is always valid.
        """
        raise NotImplementedError
