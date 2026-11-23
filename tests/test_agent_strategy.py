from metalab.action import Action, ActionType
from metalab.agent_perspective import AgentPerspective
from metalab.agent_snapshot import AgentSnapshot
from metalab.agent_strategy import AgentStrategy
from metalab.attribute import Attribute
from metalab.const.action_const import AVAILABLE_ACTIONS
from metalab.target import Target


class TestAgentStrategy:
    def test_choose_action(self):
        strategy = AgentStrategy(AVAILABLE_ACTIONS)
        state = AgentPerspective(
            own_state=AgentSnapshot(
                {
                    Attribute.HEALTH: 100,
                    Attribute.DAMAGE: 10,
                }
            ),
            enemy_state=AgentSnapshot(
                {
                    Attribute.HEALTH: 80,
                    Attribute.DAMAGE: 15,
                }
            ),
        )

        action = strategy.choose_action(state)

        assert isinstance(action, Action)
        assert action.action_type == ActionType.ATTACK
        assert action.target == Target.ENEMY
