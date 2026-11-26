
from dataclasses import FrozenInstanceError

import pytest

from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute
from metalab.battle_outcome import BattleOutcome
from metalab.battle_result import BattleResult
from metalab.battle_history import BattleHistory


@pytest.fixture
def agent_a_state():
    return AgentSnapshot({
        Attribute.HEALTH: 10,
        Attribute.DAMAGE: 3,
    })


@pytest.fixture
def agent_b_state():
    return AgentSnapshot({
        Attribute.HEALTH: 8,
        Attribute.DAMAGE: 2,
    })


@pytest.fixture
def history():
    return BattleHistory()


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
    def test_init(
        self,
        outcome,
        agent_a_state,
        agent_b_state,
        history,
    ):
        """Проверка успешной инициализации BattleResult."""
        result = BattleResult(
            outcome=outcome,
            rounds_played=5,
            agent_a_state=agent_a_state,
            agent_b_state=agent_b_state,
            history=history,
        )

        assert result.outcome is outcome
        assert result.rounds_played == 5
        assert result.agent_a_state is agent_a_state
        assert result.agent_b_state is agent_b_state
        assert result.history is history

    @pytest.mark.parametrize(
        "outcome",
        [None, "A_WON", 1, True],
    )
    def test_init_invalid_outcome(
        self,
        outcome,
        agent_a_state,
        agent_b_state,
        history,
    ):
        """Проверка отклонения некорректного типа outcome."""
        with pytest.raises(TypeError):
            BattleResult(
                outcome=outcome,
                rounds_played=5,
                agent_a_state=agent_a_state,
                agent_b_state=agent_b_state,
                history=history,
            )

    @pytest.mark.parametrize(
        "rounds_played",
        ["5", 5.5, True, None, [5]],
    )
    def test_init_invalid_rounds_played_type(
        self,
        rounds_played,
        agent_a_state,
        agent_b_state,
        history,
    ):
        """Проверка отклонения некорректного типа rounds_played."""
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=rounds_played,
                agent_a_state=agent_a_state,
                agent_b_state=agent_b_state,
                history=history,
            )

    @pytest.mark.parametrize(
        "rounds_played",
        [-1, -5],
    )
    def test_init_invalid_rounds_played_value(
        self,
        rounds_played,
        agent_a_state,
        agent_b_state,
        history,
    ):
        """Проверка отклонения отрицательного значения rounds_played."""
        with pytest.raises(ValueError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=rounds_played,
                agent_a_state=agent_a_state,
                agent_b_state=agent_b_state,
                history=history,
            )

    @pytest.mark.parametrize(
        "agent_a_state",
        [None, {}, "state", 1],
    )
    def test_init_invalid_agent_a_state(
        self,
        agent_a_state,
        agent_b_state,
        history,
    ):
        """Проверка отклонения некорректного типа agent_a_state."""
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=5,
                agent_a_state=agent_a_state,
                agent_b_state=agent_b_state,
                history=history,
            )

    @pytest.mark.parametrize(
        "agent_b_state",
        [None, {}, "state", 1],
    )
    def test_init_invalid_agent_b_state(
        self,
        agent_b_state,
        history,
    ):
        """Проверка отклонения некорректного типа agent_b_state."""
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=5,
                agent_a_state=AgentSnapshot({}),
                agent_b_state=agent_b_state,
                history=history,
            )

    @pytest.mark.parametrize(
        "history",
        [None, {}, [], "history", 1, True],
    )
    def test_init_invalid_history(
        self,
        history,
        agent_a_state,
        agent_b_state,
    ):
        """Проверка отклонения некорректного типа history."""
        with pytest.raises(TypeError):
            BattleResult(
                outcome=BattleOutcome.A_WON,
                rounds_played=5,
                agent_a_state=agent_a_state,
                agent_b_state=agent_b_state,
                history=history,
            )

    def test_immutable(
        self,
        agent_a_state,
        agent_b_state,
        history,
    ):
        """Проверка неизменяемости полей BattleResult."""
        result = BattleResult(
            outcome=BattleOutcome.A_WON,
            rounds_played=5,
            agent_a_state=agent_a_state,
            agent_b_state=agent_b_state,
            history=history,
        )

        with pytest.raises(FrozenInstanceError):
            result.rounds_played = 10

        with pytest.raises(FrozenInstanceError):
            result.history = BattleHistory()
