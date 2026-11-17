import pytest
from contextlib import nullcontext as does_not_raise
from metalab.agent_state import AgentState
from dataclasses import FrozenInstanceError
from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute


# Вспомогательная функция-конструктор для чистоты тестов
def make_snapshot(health: int, damage: int) -> AgentSnapshot:
    return AgentSnapshot(attributes={
        Attribute.HEALTH: health,
        Attribute.DAMAGE: damage
    })

@pytest.fixture
def own_snapshot() -> AgentSnapshot:
    return make_snapshot(health=5, damage=6)


@pytest.fixture
def enemy_snapshot() -> AgentSnapshot:
    return make_snapshot(health=3, damage=8)


class TestAgentState:

    @pytest.mark.parametrize("own_snap, enemy_snap, expectation", [
        (make_snapshot(5, 6), make_snapshot(3, 8), does_not_raise()),
        (make_snapshot(1, 6), make_snapshot(3, 0), does_not_raise()),
        ((4, 7), make_snapshot(3, 8), pytest.raises(TypeError)),
        (make_snapshot(3, 8), (3, 8), pytest.raises(TypeError)),
    ])
    def test_init_agent_state(self, own_snap:AgentSnapshot, enemy_snap:AgentSnapshot, expectation):
        with expectation:
            agent_state = AgentState(own_snap, enemy_snap)
            assert agent_state.own_state == own_snap
            assert agent_state.enemy_state == enemy_snap

    def test_immutable_state(self, own_snapshot, enemy_snapshot):
        agent_state = AgentState(own_state=own_snapshot, enemy_state=enemy_snapshot)

        with pytest.raises(FrozenInstanceError):
            agent_state.own_state = enemy_snapshot
