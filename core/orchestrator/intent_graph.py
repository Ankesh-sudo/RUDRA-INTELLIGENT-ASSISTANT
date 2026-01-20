from typing import List, Any
from core.orchestrator.intent_node import IntentNode


class IntentGraph:
    """
    Directed Acyclic Graph (DAG) of intent nodes.
    Used for planning only (no execution).
    """
    def __init__(self):
        self.nodes: List[IntentNode] = []

    def add_sequential(self, intents: List[Any]) -> None:
        """
        Add intents as a strictly sequential dependency chain.
        """
        previous_node: IntentNode | None = None

        for intent in intents:
            node = IntentNode(intent)
            self.nodes.append(node)

            if previous_node is not None:
                node.add_dependency(previous_node)

            previous_node = node

    def ordered_nodes(self) -> List[IntentNode]:
        """
        Return nodes in insertion order.
        """
        return self.nodes
