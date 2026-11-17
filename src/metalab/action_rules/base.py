from abc import ABC, abstractmethod

from metalab.agent_state import AgentState
from metalab.target import Target
from metalab.effect import Effect



class ActionRules(ABC):
    @abstractmethod
    def calculate_effects(self, state: AgentState, target: Target) -> tuple[Effect,...] :
        pass

# class AttackRules(ActionRules):
#
#     def rule(self, state: AgentState):
#         health = state.enemy_health
#         damage = state.own_damage
#
#         return health - damage
