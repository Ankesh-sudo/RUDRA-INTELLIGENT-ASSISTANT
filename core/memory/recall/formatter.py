from typing import Iterable
from datetime import datetime

from .recall_result import RecallResult


def _format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def format_recall_result(result: RecallResult) -> str:
    header = (
        f"[{result.category.name} | "
        f"confidence: {result.confidence:.2f} | "
        f"updated: {_format_datetime(result.last_updated)}]"
    )
    return f"{header}\n{result.content}"


def format_recall_results(results: Iterable[RecallResult]) -> str:
    results = list(results)
    if not results:
        return "No memories found."

    if len(results) == 1:
        return format_recall_result(results[0])

    lines = []
    for idx, result in enumerate(results, start=1):
        formatted = format_recall_result(result)
        indented = "\n".join("   " + line for line in formatted.splitlines())
        lines.append(f"{idx}.\n{indented}")

    return "\n\n".join(lines)
