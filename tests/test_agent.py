import pytest

from metalab.agent import Agent
from metalab.build import Build
from contextlib import nullcontext as does_not_raise


class TestAgent:
    @pytest.mark.parametrize("build", [
        (Build(6, 5)),
    ])
    def test_create_agent(self, build):
        build_from_agent = build
        agent = Agent(build_from_agent)
        assert isinstance(agent, Agent)

    def test_health(self):
        build_from_agent = Build(damage=4, health=6)
        agent = Agent(build_from_agent)
        assert agent.health == 6
        assert agent.damage == 4

    @pytest.mark.parametrize("damage", [
        1, 2, 3, 4, 5, 6, -1, 0
    ])
    def test_take_damage(self, damage):
        health = 5
        build_from_agent = Build(damage=5, health=health)
        agent = Agent(build_from_agent)
        agent.take_damage(damage)
        assert agent.health == health - damage

    @pytest.mark.parametrize("damage, is_alive", [
        (1, True),
        (2, True),
        (3, True),
        (4, False),
        (5, False),
        (-1, True),
        (0, True)
    ])
    def test_is_alive(self, damage, is_alive):
        build_from_agent = Build(damage=6, health=4)
        agent = Agent(build_from_agent)
        agent.take_damage(damage)
        assert agent.is_alive is is_alive

    @pytest.mark.parametrize("damage, expected", [
        (1, does_not_raise()),
        (2, does_not_raise()),
        ("5", pytest.raises(TypeError)),
        (5.7, pytest.raises(TypeError)),
        (True, pytest.raises(TypeError)),
    ])
    def test_take_damage_raise(self, damage, expected):
        build_from_agent = Build(damage=4, health=6)
        agent = Agent(build_from_agent)
        with expected:
            agent.take_damage(damage)

    def test_immutable(self):
        build_from_agent = Build(damage=4, health=6)
        agent = Agent(build_from_agent)
        agent.take_damage(5)
        assert agent.build.health == 6
