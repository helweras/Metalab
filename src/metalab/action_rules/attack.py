from metalab.action_result import ActionResult
from metalab.action_rules.base import ActionRules
from metalab.agent_perspective import AgentPerspective
from metalab.attribute import Attribute
from metalab.effect import Effect
from metalab.target import Target


class AttackRules(ActionRules):
    def calculate_effects(
        self, state: AgentPerspective, target: Target
    ) -> tuple[Effect, ...]:
        own_state = state.own_state.attributes
        own_damage = own_state[Attribute.DAMAGE]

        delta = -own_damage

        action_result = ActionResult(Attribute.HEALTH, delta)

        return (Effect(action_result, target),)
