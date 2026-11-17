from metalab.action_result import ActionResult
from metalab.action_rules.base import ActionRules
from metalab.agent_state import AgentState
from metalab.effect import Effect
from metalab.target import Target
from metalab.attribute import Attribute


class AttackRules(ActionRules):
    def calculate_effects(self, state: AgentState, target: Target) -> tuple[Effect, ...]:
        own_state = state.own_state.attributes
        own_damage = own_state[Attribute.DAMAGE]

        delta = -own_damage

        action_result = ActionResult(Attribute.HEALTH, delta)

        return (Effect(action_result, target),)
