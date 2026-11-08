import pytest
from contextlib import nullcontext as does_not_raise
from metalab.agent_state import AgentState
from dataclasses import FrozenInstanceError
from metalab.agent_snapshot import AgentSnapshot


class TestAgentState:

    @pytest.mark.parametrize("own_snapshot, enemy_snapshot, expectation", [
        (
                AgentSnapshot(health=5, damage=6),
                AgentSnapshot(health=3, damage=8),
                does_not_raise()
        ),

        (
                AgentSnapshot(health=1, damage=6),
                AgentSnapshot(health=3, damage=0),
                does_not_raise()
        ),
        (
                (4, 7),
                AgentSnapshot(health=3, damage=8),
                pytest.raises(TypeError),
        ),

        (
                AgentSnapshot(health=3, damage=8),
                (3, 8),
                pytest.raises(TypeError)
        ),

    ])
    def test_init_agent_state(self, own_snapshot,
                        enemy_snapshot,
                        expectation):
        with expectation:
            agent_state = AgentState(own_snapshot, enemy_snapshot)
            assert agent_state.own_state == own_snapshot
            assert agent_state.enemy_state == enemy_snapshot


    def test_immutable_state(self):
        own_state = AgentSnapshot(health=5, damage=6)
        enemy_state = AgentSnapshot(health=3, damage=8)

        agent_state = AgentState(own_state=own_state,
                                 enemy_state=enemy_state)

        with pytest.raises(FrozenInstanceError):
            agent_state.own_state = enemy_state
