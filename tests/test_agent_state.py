import pytest
from contextlib import nullcontext as does_not_raise
from metalab.agent_state import AgentState
from dataclasses import FrozenInstanceError


class TestAgentState:

    @pytest.mark.parametrize("own_health, own_damage, enemy_health, enemy_damage, expectation", [
        (4, 5, 5, 6, does_not_raise()),
        (0, 5, 5, 11, does_not_raise()),
        ("6", 5, "6", 6, pytest.raises(TypeError)),
        (True, 5, 5, 6, pytest.raises(TypeError)),
        (-7, 5, 5, 6, does_not_raise()),
    ])
    def test_init_agent(self, own_health,
                       own_damage,
                       enemy_health,
                       enemy_damage,
                       expectation):
        with expectation:
            agent_state = AgentState(own_health, own_damage, enemy_health, enemy_damage)
            assert agent_state.own_health == own_health
            assert agent_state.own_damage == own_damage
            assert agent_state.enemy_health == enemy_health
            assert agent_state.enemy_damage == enemy_damage

    def test_immutable_state(self):
        agent_state = AgentState(own_health=3,
                                 own_damage=4,
                                 enemy_health=5,
                                 enemy_damage=6)
        with pytest.raises(FrozenInstanceError):

            agent_state.own_health = 0
