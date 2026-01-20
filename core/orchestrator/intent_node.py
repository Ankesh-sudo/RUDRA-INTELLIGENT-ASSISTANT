from typing import Set, Any


class IntentNode:
    """
    Node in an Intent Graph (DAG).

    Wraps an intent object and tracks explicit dependencies.
    """
    def __init__(self, intent: Any):
        self.intent = intent
        self.dependencies: Set["IntentNode"] = set()
        self.dependents: Set["IntentNode"] = set()

    def add_dependency(self, node: "IntentNode") -> None:
        """
        Declare that this node depends on `node`.
        """
        self.dependencies.add(node)
        node.dependents.add(self)

    def __repr__(self) -> str:
        return f"<IntentNode intent={self.intent}>"
