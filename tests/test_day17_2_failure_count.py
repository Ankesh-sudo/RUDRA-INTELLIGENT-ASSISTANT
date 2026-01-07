"""
Day 17.2 — Failure Count Logic Tests

Validates:
- failure_count increments on low-confidence
- failure_count increments on UNKNOWN intent
- failure_count resets on successful execution
- clarification rotation is used
"""

from core.assistant import Assistant
from core.nlp.intent import Intent


class DummyInput:
    """Controlled input provider."""
    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0

    def read(self):
        if self.index >= len(self.inputs):
            return None
        val = self.inputs[self.index]
        self.index += 1
        return val


class DummyExecutor:
    """Executor that simulates success."""
    def __init__(self):
        self.called = False

    def execute(self, *args, **kwargs):
        self.called = True
        return {
            "executed": True,
            "success": True,
            "message": "Done",
            "args": {}
        }


def test_failure_count_increments_on_low_confidence():
    assistant = Assistant()
    assistant.input = DummyInput([
        "open",
        "do it",
        None
    ])

    assistant.action_executor = DummyExecutor()
    assistant.run()

    # Two vague inputs → two failures
    assert assistant.failure_count == 2


def test_failure_count_increments_on_unknown():
    assistant = Assistant()
    assistant.input = DummyInput([
        "blabla xyz",
        None
    ])

    assistant.action_executor = DummyExecutor()
    assistant.run()

    assert assistant.failure_count == 1


def test_failure_count_resets_on_success():
    assistant = Assistant()
    assistant.input = DummyInput([
        "open",
        "open browser google",
        None
    ])

    assistant.action_executor = DummyExecutor()
    assistant.run()

    # After successful execution, failure_count must reset
    assert assistant.failure_count == 0


def test_last_was_clarification_flag():
    assistant = Assistant()
    assistant.input = DummyInput([
        "do that",
        None
    ])

    assistant.action_executor = DummyExecutor()
    assistant.run()

    assert assistant.last_was_clarification is True
