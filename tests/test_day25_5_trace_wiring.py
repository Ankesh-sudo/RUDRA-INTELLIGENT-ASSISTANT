from datetime import datetime

from core.memory.trace_sink import MemoryTraceSink
from core.memory.trace import MemoryUsageTrace
from core.memory.usage_mode import MemoryUsageMode
from core.memory.explain import explain_last, explain_all


def test_trace_sink_records_and_explains():
    sink = MemoryTraceSink()

    trace = MemoryUsageTrace(
        permit_mode=MemoryUsageMode.ONCE,
        query_text="remember my preference",
        query_category="preference",
        result_ids=[42],
        timestamp=datetime.utcnow(),
        consumer="intelligence",
    )

    # record trace
    sink.record(trace)

    # explain last
    last = explain_last(sink)
    assert last == trace

    # explain all
    all_traces = explain_all(sink)
    assert all_traces == [trace]
