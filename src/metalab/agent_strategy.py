from metalab.action_registry import ActionRegistry
from metalab.agent_state import AgentState
from metalab.action import Action

class AgentStrategy:
    def __init__(self, action_registry: ActionRegistry):
        self.action_registry = action_registry

    def choose_action(self, state: AgentState) -> Action:
        return self.action_registry.attack