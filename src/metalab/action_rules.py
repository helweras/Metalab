from abc import ABC, abstractmethod
from metalab.agent_state import AgentState



class ActionRules(ABC):
    @abstractmethod
    def rule(self, state: AgentState):
        pass

class AttackRules(ActionRules):

    def rule(self, state: AgentState):
        health = state.enemy_health
        damage = state.own_damage

        return health - damage
