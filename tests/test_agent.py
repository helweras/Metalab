import pytest
from contextlib import nullcontext as does_not_raise

from metalab.agent import Agent
from metalab.build import Build
from metalab.attribute import Attribute
from metalab.action_result import ActionResult

class TestAgent:
    @pytest.mark.parametrize("build", [
        (Build(6, 5)),
    ])
    def test_create_agent(self, build):
        build_from_agent = build
        agent = Agent(build_from_agent)
        assert isinstance(agent, Agent)

    def test_state(self):
        agent = Agent(Build(damage=4, health=6))
        agent_state = agent.state
        assert agent_state.attributes[Attribute.HEALTH] == 6
        assert agent_state.attributes[Attribute.DAMAGE] == 4

    @pytest.mark.parametrize(
        "health_change, is_alive",
        [
            (-1, True),
            (-2, True),
            (-3, True),
            (-4, False),
            (-5, False),
            (1, True),
            (0, True),
        ],
    )
    def test_is_alive(self, health_change, is_alive):
        agent = Agent(Build(damage=6, health=4))

        agent.apply_action_result(
            ActionResult(Attribute.HEALTH, health_change)
        )

        assert agent.is_alive is is_alive

    @pytest.mark.parametrize(
        "health_change",
        [
            -1,
            -2,
            1,
            2,
            0,
        ],
    )
    def test_apply_action_result(self, health_change):
        agent = Agent(Build(damage=4, health=6))
        result = ActionResult(Attribute.HEALTH, health_change)

        agent.apply_action_result(result)

        assert agent.state.attributes[Attribute.HEALTH] == 6 + health_change

    def test_build_is_immutable(self):
        build = Build(damage=4, health=6)
        agent = Agent(build)

        agent.apply_action_result(
            ActionResult(Attribute.HEALTH, -5)
        )

        assert agent.build.health == 6
        assert agent.build.damage == 4
