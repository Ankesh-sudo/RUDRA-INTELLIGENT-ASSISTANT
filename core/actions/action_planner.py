from typing import List, Dict, Any
from core.actions.planned_action import PlannedAction
from core.orchestrator.intent_graph import IntentGraph
from core.os.action_spec import ActionSpec


class ActionPlanner:
    """
    Converts an IntentGraph into a list of PlannedActions.
    Planning only. No execution.
    """

    def __init__(self, intent_to_action: Dict[type, str]):
        """
        intent_to_action maps intent classes → action_type strings
        Example: {OpenAppIntent: "OPEN_APP"}
        """
        self.intent_to_action = intent_to_action

    def plan(self, graph: IntentGraph) -> List[PlannedAction]:
        planned: List[PlannedAction] = []
        node_to_planned: Dict[object, PlannedAction] = {}

        for node in graph.ordered_nodes():
            intent = node.intent
            intent_type = type(intent)

            if intent_type not in self.intent_to_action:
                raise ValueError(f"No action mapping for intent: {intent_type}")

            action_type = self.intent_to_action[intent_type]

            # Minimal, VALID ActionSpec (planning-only)
            action_spec = ActionSpec(
                action_type=action_type,
                category="SYSTEM",
                target=None,
                parameters={},
                risk_level="LOW",
                required_scopes=set(),
                destructive=False,
                supports_undo=False,
                requires_preview=False,
            )

            planned_action = PlannedAction(
                action_spec=action_spec,
                source_intent=intent,
            )

            node_to_planned[node] = planned_action
            planned.append(planned_action)

        # Wire dependencies
        for node, pa in node_to_planned.items():
            for dep_node in node.dependencies:
                pa.dependencies.add(node_to_planned[dep_node])

        return planned
