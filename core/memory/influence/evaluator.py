from typing import List

from core.memory.influence.contract import MemoryInfluenceContract
from core.memory.influence.noop import NoOpMemoryInfluence
from core.memory.influence.signal import InfluenceSignal
from core.memory.influence.gate import (
    evaluate_influence_gate,
    InfluenceGateDecision,
)


class MemoryInfluenceEvaluator:
    """
    Coordinates gate + influence evaluation.
    Default behavior is safe no-op.
    """

    def __init__(self, influence_impl: MemoryInfluenceContract | None = None):
        self._impl = influence_impl or NoOpMemoryInfluence()

    def evaluate(
        self,
        *,
        usage_mode: str,
        permit,
        recalled_memories: list,
        context: dict,
        trace_sink,
    ) -> List[InfluenceSignal]:
        # 1. Gate evaluation
        gate_result = evaluate_influence_gate(
            usage_mode=usage_mode,
            permit=permit,
            recalled_memories=recalled_memories,
        )

        trace_sink.emit(
            kind="memory_influence_gate",
            decision=gate_result.decision.value,
            reason=gate_result.reason,
            permit_id=gate_result.permit_id,
        )

        # 2. Gate denied → no influence
        if gate_result.decision == InfluenceGateDecision.DENY:
            trace_sink.emit(
                kind="memory_influence_evaluated",
                result="skipped",
                reason="gate denied",
            )
            return []

        # 3. Gate allowed → evaluate influence (No-Op)
        signals = self._impl.evaluate(
            recalled_memories=recalled_memories,
            permit=permit,
            usage_mode=usage_mode,
            context=context,
        )

        # 4. Trace evaluation result
        trace_sink.emit(
            kind="memory_influence_evaluated",
            result="none_applied" if not signals else "signals_generated",
            count=len(signals),
        )

        return signals
