from metalab.action import Action
from metalab.agent_state import AgentState
from metalab.effect import Effect, EffectTarget


class Attack(Action):
    def supply_effect(self, state: AgentState) -> Effect:
        return Effect(
            damage=state.own_damage,
            target=EffectTarget.ENEMY
        )