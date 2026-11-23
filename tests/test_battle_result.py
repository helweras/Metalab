from dataclasses import FrozenInstanceError

import pytest

from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute
from metalab.battle_outcome import BattleOutcome
from metalab.battle_result import BattleResult


class TestBattleResult:
    @pytest.mark.parametrize(
        "outcome",
        [
            BattleOutcome.A_WON,
            BattleOutcome.B_WON,
            BattleOutcome.BOTH_LOST,
            BattleOutcome.BOTH_WON,
        ],
    )
    def test_init(self, outcome):
        agent_a_state = AgentSnapshot(
            {
                Attribute.HEALTH: 10,
                Attribute.DAMAGE: 3,
            }
        )
        agent_b_state = AgentSnapshot(
            {
                Attribute.HEALTH: 8,
                Attribute.DAMAGE: 2,
            }
        )

        result = BattleResult(
            outcome=outcome,
            rounds_played=5,
            agent_a_state=agent_a_state,
            agent_b_state=agent_b_state,
        )

        assert result.outcome is outcome
        assert result.rounds_played == 5
        assert result.agent_a_state is agent_a_state
        assert result.agent_b_state is agent_b_state

    @pytest.mark.parametrize(
        "outcome",
        [None, "A_WON", 1, True],
    )
    def test_init_invalid_outcome(self, outcome):
        with pytest.raises(TypeError):
            BattleResult(
                outcome=outcome,
                rounds_played=5,
                agent_a_state=AgentSnapshot({}),
                agent_b_state=AgentSnapshot({}),
            )

    @pytest.mark.parametrize(
        "rounds_played",
        ["5", 5.5, True, None, [5]],
    )
    def test_init_invalid_rounds_played_type(self, rounds_played):
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=rounds_played,
                agent_a_state=AgentSnapshot({}),
                agent_b_state=AgentSnapshot({}),
            )

    @pytest.mark.parametrize(
        "rounds_played",
        [-1, -5],
    )
    def test_init_invalid_rounds_played_value(self, rounds_played):
        with pytest.raises(ValueError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=rounds_played,
                agent_a_state=AgentSnapshot({}),
                agent_b_state=AgentSnapshot({}),
            )

    @pytest.mark.parametrize(
        "agent_a_state",
        [None, {}, "state", 1],
    )
    def test_init_invalid_agent_a_state(self, agent_a_state):
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=5,
                agent_a_state=agent_a_state,
                agent_b_state=AgentSnapshot({}),
            )

    @pytest.mark.parametrize(
        "agent_b_state",
        [None, {}, "state", 1],
    )
    def test_init_invalid_agent_b_state(self, agent_b_state):
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=5,
                agent_a_state=AgentSnapshot({}),
                agent_b_state=agent_b_state,
            )

    def test_immutable(self):
        result = BattleResult(
            outcome=BattleOutcome.A_WON,
            rounds_played=5,
            agent_a_state=AgentSnapshot({}),
            agent_b_state=AgentSnapshot({}),
        )

        with pytest.raises(FrozenInstanceError):
            result.rounds_played = 10
