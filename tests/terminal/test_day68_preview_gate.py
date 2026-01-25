# tests/terminal/test_day68_preview_gate.py

from core.terminal.command_spec import TerminalCommandSpec
from core.terminal.terminal_sandbox import TerminalSandbox
from core.terminal.terminal_preview_flow import TerminalPreviewFlow
from core.terminal.confirm_gate import ConfirmationGate


def test_dry_run_preview_render():
    spec = TerminalCommandSpec(command="uptime", reason="Check system uptime")
    vr = TerminalSandbox.validate(spec)
    preview = TerminalPreviewFlow.preview(spec, vr)

    text = preview.render()
    assert "uptime" in text
    assert "read-only" not in text  # human wording only


def test_confirmation_gate_yes_only():
    assert ConfirmationGate.confirm("YES") is True
    assert ConfirmationGate.confirm("yes") is False
    assert ConfirmationGate.confirm("Y") is False
