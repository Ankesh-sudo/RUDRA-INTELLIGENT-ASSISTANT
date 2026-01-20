from core.orchestrator.intent_graph import IntentGraph


class DummyIntent:
    """
    Minimal stub for testing IntentGraph.
    """
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<DummyIntent {self.name}>"


def test_sequential_graph_dependencies():
    i1 = DummyIntent("open chrome")
    i2 = DummyIntent("search instagram")
    i3 = DummyIntent("open login page")

    graph = IntentGraph()
    graph.add_sequential([i1, i2, i3])

    nodes = graph.ordered_nodes()
    n1, n2, n3 = nodes

    assert n1.dependencies == set()
    assert n2.dependencies == {n1}
    assert n3.dependencies == {n2}


def test_graph_node_count():
    intents = [
        DummyIntent("open chrome"),
        DummyIntent("search instagram"),
    ]

    graph = IntentGraph()
    graph.add_sequential(intents)

    assert len(graph.ordered_nodes()) == 2


def test_graph_single_node():
    intent = DummyIntent("open chrome")

    graph = IntentGraph()
    graph.add_sequential([intent])

    nodes = graph.ordered_nodes()

    assert len(nodes) == 1
    assert nodes[0].dependencies == set()


def test_graph_empty_input():
    graph = IntentGraph()
    graph.add_sequential([])

    assert graph.ordered_nodes() == []
