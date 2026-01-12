from datetime import datetime
import pytest

from core.memory.trace import MemoryUsageTrace
from core.memory.usage_mode import MemoryUsageMode


def test_trace_is_immutable():
    trace = MemoryUsageTrace(
        permit_mode=MemoryUsageMode.ONCE,
        query_text="test memory",
        query_category="preference",
        result_ids=[1, 2, 3],
        timestamp=datetime.utcnow(),
        consumer="intelligence",
    )

    with pytest.raises(Exception):
        trace.consumer = "other"
