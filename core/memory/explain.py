from typing import Optional, List

from core.memory.trace import MemoryUsageTrace
from core.memory.trace_sink import MemoryTraceSink


def explain_last(trace_sink: MemoryTraceSink) -> Optional[MemoryUsageTrace]:
    """
    Return the most recent memory usage trace.

    This answers:
    'Why did you say that?'

    Returns:
        MemoryUsageTrace if available, else None
    """
    traces = trace_sink.fetch_all()
    if not traces:
        return None
    return traces[-1]


def explain_all(trace_sink: MemoryTraceSink) -> List[MemoryUsageTrace]:
    """
    Return all memory usage traces for the current session.

    Read-only access.
    No mutation.
    """
    return trace_sink.fetch_all()
