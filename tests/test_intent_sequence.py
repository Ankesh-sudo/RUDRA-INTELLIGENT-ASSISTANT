# tests/test_intent_sequence.py

from core.intelligence.intent_sequence import IntentSequence


class DummyIntent:
    """
    Minimal stub that satisfies the IntentSequence contract.
    Only sequence_index matters here.
    """
    def __init__(self, name: str, sequence_index: int):
        self.name = name
        self.sequence_index = sequence_index

    def __repr__(self):
        return f"<DummyIntent {self.name} ({self.sequence_index})>"


def test_intent_sequence_orders_by_sequence_index():
    intent1 = DummyIntent("open chrome", 2)
    intent2 = DummyIntent("search instagram", 1)
    intent3 = DummyIntent("open login page", 3)

    sequence = IntentSequence([intent1, intent2, intent3])
    ordered = sequence.ordered()

    assert ordered == [intent2, intent1, intent3]


def test_intent_sequence_preserves_order_when_already_sorted():
    intent1 = DummyIntent("open chrome", 0)
    intent2 = DummyIntent("search instagram", 1)

    sequence = IntentSequence([intent1, intent2])
    ordered = sequence.ordered()

    assert ordered == [intent1, intent2]


def test_intent_sequence_with_single_intent():
    intent = DummyIntent("open chrome", 0)

    sequence = IntentSequence([intent])
    ordered = sequence.ordered()

    assert ordered == [intent]


def test_intent_sequence_empty_list():
    sequence = IntentSequence([])
    ordered = sequence.ordered()

    assert ordered == []
