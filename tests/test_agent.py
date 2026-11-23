import pytest

from metalab.action_result import ActionResult
from metalab.agent import Agent
from metalab.attribute import Attribute
from metalab.build import Build


class TestAgent:
    def test_create_agent(self):
        """Проверяет создание агента."""
        agent = Agent(Build(damage=6, health=5))

        assert isinstance(agent, Agent)

    def test_state(self):
        """Проверяет начальные характеристики агента."""
        agent = Agent(Build(damage=4, health=6))

        assert agent.snapshot.attributes[Attribute.HEALTH] == 6
        assert agent.snapshot.attributes[Attribute.DAMAGE] == 4

    @pytest.mark.parametrize(
        ("health_change", "is_alive"),
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
        """Проверяет состояние жизни агента после изменения здоровья."""
        agent = Agent(Build(damage=6, health=4))

        agent.apply_action_result(ActionResult(Attribute.HEALTH, health_change))

        assert agent.is_alive is is_alive

    @pytest.mark.parametrize(
        ("health_change", "expected_health"),
        [(-1, 5), (-3, 3), (-6, 0), (1, 6), (5, 6), (-7, -1)],
    )
    def test_apply_action_result(self, health_change, expected_health):
        """Проверяет изменение здоровья с учетом максимального значения."""
        agent = Agent(Build(damage=4, health=6))

        agent.apply_action_result(ActionResult(Attribute.HEALTH, health_change))

        assert agent.snapshot.attributes[Attribute.HEALTH] == expected_health

    def test_build_is_immutable(self):
        """Проверяет, что изменение состояния агента не меняет его сборку."""
        build = Build(damage=4, health=6)
        agent = Agent(build)

        agent.apply_action_result(ActionResult(Attribute.HEALTH, -5))

        assert agent.build.health == 6
        assert agent.build.damage == 4

    @pytest.mark.parametrize(
        ("damage", "healing", "expected_health"),
        [
            (3, 2, 5),
            (5, 10, 6),
            (1, 1, 6),
        ],
    )
    def test_apply_action_result_damage_and_healing(
        self, damage, healing, expected_health
    ):
        """Проверяет последовательное получение урона и лечение."""
        agent = Agent(Build(damage=4, health=6))

        agent.apply_action_result(ActionResult(Attribute.HEALTH, -damage))
        agent.apply_action_result(ActionResult(Attribute.HEALTH, healing))

        assert agent.snapshot.attributes[Attribute.HEALTH] == expected_health

    @pytest.mark.parametrize(
        "invalid_action_result",
        [
            None,
            10,
            "invalid",
            object(),
        ],
    )
    def test_apply_action_result_with_invalid_argument(self, invalid_action_result):
        """Проверяет ошибку при передаче некорректного аргумента."""
        agent = Agent(Build(damage=4, health=6))

        with pytest.raises(
            TypeError,
            match="action_result must be an ActionResult",
        ):
            agent.apply_action_result(invalid_action_result)
