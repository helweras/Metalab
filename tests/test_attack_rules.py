
import pytest

from metalab.action_rules.attack import AttackRules
from metalab.agent_state import AgentState
from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute
from metalab.effect import Effect
from metalab.target import Target


class TestAttackRules:
    @pytest.mark.parametrize(
        "damage, target",
        [
            (1, Target.ENEMY),
            (2, Target.ENEMY),
            (5, Target.ENEMY),
            (10, Target.SELF),
        ],
    )
    def test_calculate_effects(self, damage, target):
        state = AgentState(
            own_state=AgentSnapshot({
                Attribute.HEALTH: 100,
                Attribute.DAMAGE: damage,
            }),
            enemy_state=AgentSnapshot({
                Attribute.HEALTH: 100,
                Attribute.DAMAGE: 3,
            }),
        )

        rules = AttackRules()

        effects = rules.calculate_effects(state, target)

        assert isinstance(effects, tuple)
        assert len(effects) == 1

        effect = effects[0]

        assert isinstance(effect, Effect)
        assert effect.action_result.attribute == Attribute.HEALTH
        assert effect.action_result.value == -damage
        assert effect.target == target
