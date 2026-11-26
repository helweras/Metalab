
import pytest

from metalab.action import Action
from metalab.action_result import ActionResult
from metalab.agent import Agent
from metalab.attribute import Attribute
from metalab.battle_history import BattleHistory
from metalab.battle_history_formatter import BattleHistoryFormatter
from metalab.battle_outcome import BattleOutcome
from metalab.battle_result import BattleResult
from metalab.build import Build
from metalab.effect import Effect
from metalab.round_record import RoundRecord
from metalab.target import Target
from metalab.const.action_const import AVAILABLE_ACTIONS


class TestBattleHistoryFormatter:

    @staticmethod
    def create_snapshot(damage=4, health=8):
        return Agent(Build(damage=damage, health=health)).snapshot

    @staticmethod
    def create_record():
        agent_a_before = TestBattleHistoryFormatter.create_snapshot(
            damage=4,
            health=8,
        )
        agent_b_before = TestBattleHistoryFormatter.create_snapshot(
            damage=3,
            health=9,
        )

        agent_a_after = TestBattleHistoryFormatter.create_snapshot(
            damage=4,
            health=6,
        )
        agent_b_after = TestBattleHistoryFormatter.create_snapshot(
            damage=3,
            health=7,
        )

        action_a = Action(AVAILABLE_ACTIONS[0], Target.ENEMY)
        action_b = Action(AVAILABLE_ACTIONS[0], Target.ENEMY)

        effects_a = (
            Effect(
                ActionResult(Attribute.HEALTH, -2),
                Target.ENEMY,
            ),
        )

        effects_b = (
            Effect(
                ActionResult(Attribute.HEALTH, -2),
                Target.ENEMY,
            ),
        )

        return RoundRecord(
            round_number=1,
            agent_a_before=agent_a_before,
            agent_b_before=agent_b_before,
            action_a=action_a,
            action_b=action_b,
            effects_a=effects_a,
            effects_b=effects_b,
            agent_a_after=agent_a_after,
            agent_b_after=agent_b_after,
        )

    @staticmethod
    def create_result(history=None):
        if history is None:
            history = BattleHistory(
                rounds=(TestBattleHistoryFormatter.create_record(),)
            )

        return BattleResult(
            outcome=BattleOutcome.A_WON,
            rounds_played=history.total_rounds,
            agent_a_state=TestBattleHistoryFormatter.create_snapshot(
                damage=4,
                health=6,
            ),
            agent_b_state=TestBattleHistoryFormatter.create_snapshot(
                damage=3,
                health=1,
            ),
            history=history,
        )

    def test_format_returns_string(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert isinstance(output, str)

    def test_format_contains_battle_result(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "РЕЗУЛЬТАТ БОЯ" in output
        assert "Исход: A_WON" in output
        assert "Раундов проведено: 1" in output

    def test_format_contains_final_agent_states(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "ФИНАЛЬНОЕ СОСТОЯНИЕ АГЕНТОВ" in output
        assert "Агент А: HEALTH=6, DAMAGE=4" in output
        assert "Агент Б: HEALTH=1, DAMAGE=3" in output

    def test_format_contains_round_history(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "ИСТОРИЯ БОЯ" in output
        assert "РАУНД 1" in output

    def test_format_contains_initial_round_states(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "СОСТОЯНИЕ В НАЧАЛЕ РАУНДА" in output
        assert "Агент А: HEALTH=8, DAMAGE=4" in output
        assert "Агент Б: HEALTH=9, DAMAGE=3" in output

    def test_format_contains_actions_and_targets(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "ДЕЙСТВИЕ АГЕНТА А" in output
        assert "ДЕЙСТВИЕ АГЕНТА Б" in output
        assert f"Действие: {AVAILABLE_ACTIONS[0].name}" in output
        assert "Цель: ENEMY" in output

    def test_format_contains_effects(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "Эффекты: ENEMY: HEALTH -2" in output

    def test_format_contains_final_round_states(self):
        formatter = BattleHistoryFormatter()
        result = self.create_result()

        output = formatter.format(result)

        assert "СОСТОЯНИЕ ПОСЛЕ РАУНДА" in output
        assert "Агент А: HEALTH=6, DAMAGE=4" in output
        assert "Агент Б: HEALTH=7, DAMAGE=3" in output

    def test_format_empty_history(self):
        formatter = BattleHistoryFormatter()
        history = BattleHistory(rounds=())
        result = self.create_result(history)

        output = formatter.format(result)

        assert "История боя пуста." in output

    def test_format_raises_type_error_for_invalid_result(self):
        formatter = BattleHistoryFormatter()

        with pytest.raises(TypeError):
            formatter.format("не результат боя")

    def test_format_round_returns_list(self):
        formatter = BattleHistoryFormatter()
        record = self.create_record()

        output = formatter._format_round(record)

        assert isinstance(output, list)

    def test_format_round_raises_type_error_for_invalid_record(self):
        formatter = BattleHistoryFormatter()

        with pytest.raises(TypeError):
            formatter._format_round("не запись раунда")

    def test_format_snapshot_returns_string(self):
        formatter = BattleHistoryFormatter()
        snapshot = self.create_snapshot()

        output = formatter._format_snapshot(snapshot)

        assert isinstance(output, str)
        assert "HEALTH=8" in output
        assert "DAMAGE=4" in output

    def test_format_snapshot_raises_type_error_for_invalid_snapshot(self):
        formatter = BattleHistoryFormatter()

        with pytest.raises(TypeError):
            formatter._format_snapshot("не снимок")

    def test_format_effects_returns_string(self):
        formatter = BattleHistoryFormatter()
        record = self.create_record()

        output = formatter._format_effects(record.effects_a)

        assert output == "ENEMY: HEALTH -2"

    def test_format_empty_effects(self):
        formatter = BattleHistoryFormatter()

        output = formatter._format_effects(())

        assert output == "Нет"

    def test_format_effects_raises_type_error_for_invalid_type(self):
        formatter = BattleHistoryFormatter()

        with pytest.raises(TypeError):
            formatter._format_effects([])

    def test_format_effects_raises_type_error_for_invalid_element(self):
        formatter = BattleHistoryFormatter()

        with pytest.raises(TypeError):
            formatter._format_effects(("не эффект",))
