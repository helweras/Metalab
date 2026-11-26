
from dataclasses import FrozenInstanceError, replace

import pytest

from metalab.action import Action
from metalab.action_result import ActionResult
from metalab.agent import Agent
from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute
from metalab.build import Build
from metalab.const.action_const import AVAILABLE_ACTIONS
from metalab.effect import Effect
from metalab.round_record import RoundRecord
from metalab.target import Target


class TestRoundRecord:
    """Тесты валидации записи раунда."""

    @staticmethod
    def create_record():
        """Создаёт запись раунда с реальными объектами."""
        agent_a = Agent(Build(damage=5, health=7))
        agent_b = Agent(Build(damage=3, health=9))

        action_a = Action(
            action_type=AVAILABLE_ACTIONS[0],
            target=Target.ENEMY,
        )
        action_b = Action(
            action_type=AVAILABLE_ACTIONS[0],
            target=Target.ENEMY,
        )

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

    # Создание записи

    def test_create_record(self):
        """Проверяет создание корректной записи раунда."""
        record = self.create_record()

        assert record.round_number == 1

        assert isinstance(record.agent_a_before, AgentSnapshot)
        assert isinstance(record.agent_b_before, AgentSnapshot)
        assert isinstance(record.agent_a_after, AgentSnapshot)
        assert isinstance(record.agent_b_after, AgentSnapshot)

        assert isinstance(record.action_a, Action)
        assert isinstance(record.action_b, Action)

        assert len(record.effects_a) == 1
        assert len(record.effects_b) == 1

    def test_create_record_with_empty_effects(self):
        """Проверяет создание записи без эффектов."""
        record = self.create_record()

        record = replace(
            record,
            effects_a=(),
            effects_b=(),
        )

        assert record.effects_a == ()
        assert record.effects_b == ()

    # Номер раунда

    @pytest.mark.parametrize(
        "round_number",
        [None, "1", 1.5, [], {}, True, False],
    )
    def test_invalid_round_number_type(self, round_number):
        """Проверяет тип номера раунда."""
        record = self.create_record()

        with pytest.raises(
            TypeError,
            match="round_number must be an integer",
        ):
            replace(record, round_number=round_number)

    @pytest.mark.parametrize(
        "round_number",
        [0, -1, -10],
    )
    def test_invalid_round_number_value(self, round_number):
        """Проверяет допустимое значение номера раунда."""
        record = self.create_record()

        with pytest.raises(
            ValueError,
            match="round_number must be greater than or equal to 1",
        ):
            replace(record, round_number=round_number)

    # Снимки агентов

    @pytest.mark.parametrize(
        "field_name",
        [
            "agent_a_before",
            "agent_b_before",
            "agent_a_after",
            "agent_b_after",
        ],
    )
    def test_invalid_snapshot(self, field_name):
        """Проверяет типы снимков агентов."""
        record = self.create_record()

        with pytest.raises(
            TypeError,
            match=f"{field_name} must be an AgentSnapshot",
        ):
            replace(record, **{field_name: object()})

    # Действия

    @pytest.mark.parametrize(
        "field_name",
        ["action_a", "action_b"],
    )
    def test_invalid_action(self, field_name):
        """Проверяет типы действий."""
        record = self.create_record()

        with pytest.raises(
            TypeError,
            match=f"{field_name} must be an Action",
        ):
            replace(record, **{field_name: object()})

    # Эффекты

    @pytest.mark.parametrize(
        "field_name",
        ["effects_a", "effects_b"],
    )
    def test_effects_must_be_tuple(self, field_name):
        """Проверяет, что эффекты передаются кортежем."""
        record = self.create_record()

        with pytest.raises(
            TypeError,
            match=f"{field_name} must be a tuple",
        ):
            replace(record, **{field_name: []})

    @pytest.mark.parametrize(
        "field_name",
        ["effects_a", "effects_b"],
    )
    def test_effects_must_contain_effect_instances(self, field_name):
        """Проверяет типы элементов кортежа эффектов."""
        record = self.create_record()

        with pytest.raises(
            TypeError,
            match=f"all items in {field_name} must be Effect instances",
        ):
            replace(record, **{field_name: (object(),)})

    # Неизменяемость

    def test_record_is_immutable(self):
        """Проверяет неизменяемость записи раунда."""
        record = self.create_record()

        with pytest.raises(FrozenInstanceError):
            record.round_number = 2
