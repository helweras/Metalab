from metalab.agent import Agent
from metalab.agent_strategy import AgentStrategy
from metalab.agent_state import AgentState
from metalab.effect import Effect, EffectTarget
from metalab.action_rules import AttackRules


class BattleEngine:
    def __init__(
            self,
            agent_a: Agent,
            agent_b: Agent,
            strategy_a: AgentStrategy,
            strategy_b: AgentStrategy,
    ):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.strategy_a = strategy_a
        self.strategy_b = strategy_b

    def change_state(
            self,
            state_a: AgentState,
            state_b: AgentState,
            effect_a: Effect,
            effect_b: Effect
    ):

        pass



    def run_round(self):
        state_a = AgentState(own_health=self.agent_a.health,
                             own_damage=self.agent_a.damage,
                             enemy_health=self.agent_b.health,
                             enemy_damage=self.agent_b.damage)

        state_b = AgentState(own_health=self.agent_b.health,
                             own_damage=self.agent_b.damage,
                             enemy_health=self.agent_a.health,
                             enemy_damage=self.agent_a.damage)

        effect_a = self.strategy_a.choose_action(state_a)
        effect_b = self.strategy_b.choose_action(state_b)
