from abc import ABC, abstractmethod
from typing import Any


class ExecutorContract(ABC):
    @abstractmethod
    def execute(self, action_spec: Any) -> Any:
        """
        Execute (or plan) an OS action.

        Must return an ExecutionPlan-like object.
        Must never perform real OS side effects.
        """
        raise NotImplementedError
