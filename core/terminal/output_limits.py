# core/terminal/output_limits.py

from dataclasses import dataclass


@dataclass(frozen=True)
class OutputLimits:
    """
    Output constraints for terminal observation commands.
    These are declarative limits, not enforcement logic.
    """

    max_bytes: int = 16_384      # 16 KB
    max_lines: int = 200
    truncation_policy: str = "EXPLAIN"  # EXPLAIN | REJECT
