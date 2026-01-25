# core/terminal/terminal_preview_flow.py

from core.terminal.dry_run_preview import DryRunPreview
from core.terminal.confirm_gate import ConfirmationGate
from core.terminal.abort_conditions import AbortReason


class TerminalPreviewFlow:
    """
    Dry-run → confirm → abort-only gate.
    NO execution.
    """

    @staticmethod
    def preview(spec, validation_result) -> DryRunPreview:
        return DryRunPreview(
            command=validation_result.command,
            args=validation_result.args,
            why_allowed="Command is explicitly permitted for safe system observation",
            what_will_be_observed=spec.reason or "System state observation only",
        )

    @staticmethod
    def confirm_or_abort(user_input: str) -> bool:
        return ConfirmationGate.confirm(user_input)
