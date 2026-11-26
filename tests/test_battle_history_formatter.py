

import pytest

from metalab.action import Action
from metalab.action_result import ActionResult
from metalab.agent import Agent
from metalab.attribute import Attribute
from metalab.battle_history import BattleHistory
from metalab.battle_history_formatter import BattleHistoryFormatter
from metalab.build import Build
from metalab.const.action_const import AVAILABLE_ACTIONS
from metalab.effect import Effect
from metalab.round_record import RoundRecord
from metalab.target import Target


class TestBattleHistoryFormatter:
    """Тесты форматирования истории боя."""

    @staticmethod
    def create_record():
        """Создаёт запись раунда с реальными объектами."""
        agent_a = Agent(Build(damage=5, health=7))
        agent_b = Agent(Build(damage=3, health=9))

        action_a = Action(AVAILABLE_ACTIONS[0], Target.ENEMY)
        action_b = Action(AVAILABLE_ACTIONS[0], Target.ENEMY)

        effect_a = Effect(
            ActionResult(Attribute.HEALTH, -2),
            Target.ENEMY,
        )
        effect_b = Effect(
            ActionResult(Attribute.HEALTH, -3),
            Target.ENEMY,
        )

        return RoundRecord(
            round_number=1,
            agent_a_before=agent_a.snapshot,
            agent_b_before=agent_b.snapshot,
            action_a=action_a,
            action_b=action_b,
            effects_a=(effect_a,),
            effects_b=(effect_b,),
            agent_a_after=agent_a.snapshot,
            agent_b_after=agent_b.snapshot,
        )

    @staticmethod
    def create_history():
        """Создаёт историю с одним раундом."""
        return BattleHistory(rounds=(TestBattleHistoryFormatter.create_record(),))

    @staticmethod
    def create_formatter():
        """Создаёт форматтер."""
        return BattleHistoryFormatter()

    # Форматирование истории

    def test_format_history(self):
        """Проверяет форматирование истории боя."""
        formatter = self.create_formatter()
        history = self.create_history()

        result = formatter.format(history)

        assert "========== ИСТОРИЯ БОЯ ==========" in result
        assert "Всего раундов: 1" in result
        assert "========== РАУНД 1 ==========" in result
        assert "АГЕНТ А" in result
        assert "АГЕНТ Б" in result
        assert "Действие:" in result
        assert "Цель: ENEMY" in result
        assert "Эффекты: ENEMY: HEALTH -2" in result
        assert "Эффекты: ENEMY: HEALTH -3" in result
        assert "=================================" in result

    def test_format_empty_history(self):
        """Проверяет форматирование пустой истории."""
        formatter = self.create_formatter()
        history = BattleHistory(rounds=())

        assert formatter.format(history) == "История боя пуста."

    def test_format_invalid_history(self):
        """Проверяет отклонение некорректной истории."""
        formatter = self.create_formatter()

        with pytest.raises(
            TypeError,
            match="history должен иметь тип BattleHistory",
        ):
            formatter.format(None)

    # Форматирование раунда

    def test_format_round(self):
        """Проверяет форматирование отдельного раунда."""
        formatter = self.create_formatter()
        record = self.create_record()

        result = formatter._format_round(record)

        assert "========== РАУНД 1 ==========" in result
        assert "АГЕНТ А" in result
        assert "АГЕНТ Б" in result

    def test_format_round_invalid_record(self):
        """Проверяет отклонение некорректной записи раунда."""
        formatter = self.create_formatter()

        with pytest.raises(
            TypeError,
            match="record должен иметь тип RoundRecord",
        ):
            formatter._format_round(None)

    # Форматирование снимка

    def test_format_snapshot(self):
        """Проверяет форматирование снимка агента."""
        formatter = self.create_formatter()
        agent = Agent(Build(damage=5, health=7))

        result = formatter._format_snapshot(agent.snapshot)

        assert "HEALTH=7" in result
        assert "DAMAGE=5" in result

    def test_format_snapshot_invalid_type(self):
        """Проверяет отклонение некорректного снимка."""
        formatter = self.create_formatter()

        with pytest.raises(
            TypeError,
            match="snapshot должен иметь тип AgentSnapshot",
        ):
            formatter._format_snapshot(None)

    # Форматирование эффектов

    def test_format_effects(self):
        """Проверяет форматирование эффектов."""
        formatter = self.create_formatter()

        effects = (
            Effect(
                ActionResult(Attribute.HEALTH, -2),
                Target.ENEMY,
            ),
            Effect(
                ActionResult(Attribute.HEALTH, 3),
                Target.SELF,
            ),
        )

        result = formatter._format_effects(effects)

        assert result == "ENEMY: HEALTH -2; SELF: HEALTH +3"

    def test_format_empty_effects(self):
        """Проверяет форматирование пустого набора эффектов."""
        formatter = self.create_formatter()

        assert formatter._format_effects(()) == "Нет"

    @pytest.mark.parametrize(
        "effects",
        [None, [], {}, "effects", 1, True],
    )
    def test_format_effects_invalid_type(self, effects):
        """Проверяет отклонение некорректного типа effects."""
        formatter = self.create_formatter()

        with pytest.raises(
            TypeError,
            match="effects должен быть кортежем",
        ):
            formatter._format_effects(effects)

    def test_format_effects_invalid_item(self):
        """Проверяет отклонение некорректного элемента effects."""
        formatter = self.create_formatter()

        with pytest.raises(
            TypeError,
            match="Все элементы effects должны иметь тип Effect",
        ):
            formatter._format_effects((object(),))
