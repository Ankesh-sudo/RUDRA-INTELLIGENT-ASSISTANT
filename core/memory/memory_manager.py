"""
Memory Manager

Single entry point for memory writes.
Enforces policy → routes to STM / LTM.
"""

from core.memory.memory_policy import MemoryDecisionEngine, MemoryType
from core.memory.short_term_memory import ShortTermMemory
from core.memory.long_term_memory import LongTermMemory


class MemoryManager:
    def __init__(self):
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()

    def consider(
        self,
        *,
        role: str,
        content: str,
        intent: str,
        confidence: float,
        content_type: str
    ):
        decision = MemoryDecisionEngine.decide(
            intent_name=intent,
            confidence=confidence,
            content_type=content_type
        )

        if decision == MemoryType.STM:
            self.stm.store(
                role=role,
                content=content,
                intent=intent,
                confidence=confidence
            )

        elif decision == MemoryType.LTM:
            self.ltm.store(
                content=content,
                memory_type=content_type,
                confidence=confidence
            )
