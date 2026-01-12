from datetime import datetime

from core.memory.recall.formatter import (
    format_recall_result,
    format_recall_results,
)
from core.memory.recall.recall_result import RecallResult
from core.memory.types import MemoryCategory


def make_result():
    return RecallResult(
        memory_id="1",
        category=MemoryCategory.FACT,
        content="Laptop has 16GB RAM",
        confidence=0.9234,
        created_at=datetime(2026, 1, 1, 10, 0),
        last_updated=datetime(2026, 1, 10, 12, 30),
    )


def test_single_result_formatting():
    result = make_result()
    text = format_recall_result(result)

    assert "FACT" in text
    assert "0.92" in text
    assert "Laptop has 16GB RAM" in text
    assert "2026-01-10" in text


def test_multiple_results_formatting():
    r1 = make_result()
    r2 = RecallResult(
        memory_id="2",
        category=MemoryCategory.PREFERENCE,
        content="Prefers dark theme",
        confidence=0.9,
        created_at=r1.created_at,
        last_updated=r1.last_updated,
    )

    text = format_recall_results([r1, r2])

    assert "1." in text
    assert "2." in text
    assert "Prefers dark theme" in text


def test_empty_results():
    text = format_recall_results([])
    assert text == "No memories found."
