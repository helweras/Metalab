from abc import ABC, abstractmethod
from metalab.agent_state import AgentState
from metalab.effect import Effect


class Action(ABC):
    @abstractmethod
    def supply_effect(self, state: AgentState) -> Effect:
        pass
