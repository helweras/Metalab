
import pytest

from metalab.action_result import ActionResult
from metalab.agent import Agent
from metalab.agent_strategy import AgentStrategy
from metalab.attribute import Attribute
from metalab.battle_engine import BattleEngine
from metalab.battle_outcome import BattleOutcome
from metalab.battle_rules import BattleRules
from metalab.battle_settings import BattleSettings
from metalab.build import Build
from metalab.action_rules_registry import ActionRulesRegistry
from metalab.effect import Effect
from metalab.target import Target
from metalab.const.action_const import AVAILABLE_ACTIONS


class TestBattleEngine:
    """Тесты применения эффектов и выполнения боевых сценариев."""

    @staticmethod
    def create_engine(max_rounds=5):
        """Создает боевой движок с заданным ограничением раундов."""
        return BattleEngine(
            action_rules=ActionRulesRegistry(),
            battle_rules=BattleRules(BattleSettings(max_rounds)),
        )

    @staticmethod
    def create_strategy():
        """Создает стратегию со всеми доступными действиями."""
        return AgentStrategy(AVAILABLE_ACTIONS)

    # Применение эффектов

    def test_apply_effects_to_self(self):
        """Проверяет применение эффекта к самому источнику."""
        engine = self.create_engine()
        agent = Agent(Build(damage=5, health=6))
        enemy = Agent(Build(damage=3, health=8))

        effect = Effect(
            ActionResult(Attribute.HEALTH, -4),
            Target.SELF,
        )

        engine.apply_effects(agent, enemy, (effect,))

        assert agent.snapshot.attributes[Attribute.HEALTH] == 2
        assert enemy.snapshot.attributes[Attribute.HEALTH] == 8

    def test_apply_effects_to_enemy(self):
        """Проверяет применение эффекта к противнику."""
        engine = self.create_engine()
        agent = Agent(Build(damage=5, health=6))
        enemy = Agent(Build(damage=3, health=8))

        effect = Effect(
            ActionResult(Attribute.HEALTH, -4),
            Target.ENEMY,
        )

        engine.apply_effects(agent, enemy, (effect,))

        assert agent.snapshot.attributes[Attribute.HEALTH] == 6
        assert enemy.snapshot.attributes[Attribute.HEALTH] == 4

    def test_apply_multiple_effects(self):
        """Проверяет последовательное применение нескольких эффектов."""
        engine = self.create_engine()
        agent = Agent(Build(damage=5, health=6))
        enemy = Agent(Build(damage=3, health=8))

        effects = (
            Effect(ActionResult(Attribute.HEALTH, -2), Target.SELF),
            Effect(ActionResult(Attribute.HEALTH, -3), Target.ENEMY),
            Effect(ActionResult(Attribute.HEALTH, -1), Target.SELF),
        )

        engine.apply_effects(agent, enemy, effects)

        assert agent.snapshot.attributes[Attribute.HEALTH] == 3
        assert enemy.snapshot.attributes[Attribute.HEALTH] == 5

    def test_apply_empty_effects(self):
        """Проверяет, что пустой набор эффектов не изменяет состояние агентов."""
        engine = self.create_engine()
        agent = Agent(Build(damage=5, health=6))
        enemy = Agent(Build(damage=3, health=8))

        engine.apply_effects(agent, enemy, ())

        assert agent.snapshot.attributes[Attribute.HEALTH] == 6
        assert enemy.snapshot.attributes[Attribute.HEALTH] == 8

    # Выполнение боя

    def test_start_battle_both_agents_survive_max_rounds(self):
        """Проверяет завершение боя по достижении максимального числа раундов."""
        engine = self.create_engine(max_rounds=1)

        agent_a = Agent(Build(damage=3, health=8))
        agent_b = Agent(Build(damage=4, health=7))

        result = engine.start_battle(
            agent_a,
            agent_b,
            self.create_strategy(),
            self.create_strategy(),
        )

        assert result.outcome is BattleOutcome.BOTH_WON
        assert result.rounds_played == 1
        assert result.agent_a_state.attributes[Attribute.HEALTH] == 4
        assert result.agent_b_state.attributes[Attribute.HEALTH] == 4

    def test_start_battle_applies_second_action_after_agent_b_dies(self):
        """Проверяет применение обоих действий, даже если первая атака смертельна."""
        engine = self.create_engine()

        agent_a = Agent(Build(damage=6, health=6))
        agent_b = Agent(Build(damage=6, health=6))

        result = engine.start_battle(
            agent_a,
            agent_b,
            self.create_strategy(),
            self.create_strategy(),
        )

        assert result.outcome is BattleOutcome.BOTH_LOST
        assert result.rounds_played == 1
        assert result.agent_a_state.attributes[Attribute.HEALTH] == 0
        assert result.agent_b_state.attributes[Attribute.HEALTH] == 0

    def test_start_battle_agent_a_loses(self):
        """Проверяет победу агента B при гибели агента A."""
        engine = self.create_engine()

        agent_a = Agent(Build(damage=2, health=8))
        agent_b = Agent(Build(damage=8, health=3))

        result = engine.start_battle(
            agent_a,
            agent_b,
            self.create_strategy(),
            self.create_strategy(),
        )

        assert result.outcome is BattleOutcome.B_WON
        assert result.rounds_played == 1
        assert result.agent_a_state.attributes[Attribute.HEALTH] == 0
        assert result.agent_b_state.attributes[Attribute.HEALTH] == 1

    def test_start_battle_agent_b_loses(self):
        """Проверяет победу агента A при гибели агента B."""
        engine = self.create_engine()

        agent_a = Agent(Build(damage=8, health=3))
        agent_b = Agent(Build(damage=2, health=8))

        result = engine.start_battle(
            agent_a,
            agent_b,
            self.create_strategy(),
            self.create_strategy(),
        )

        assert result.outcome is BattleOutcome.A_WON
        assert result.rounds_played == 1
        assert result.agent_a_state.attributes[Attribute.HEALTH] == 1
        assert result.agent_b_state.attributes[Attribute.HEALTH] == 0

    # Проверка входных условий

    def test_start_battle_agent_cannot_fight_itself(self):
        """Проверяет запрет боя агента с самим собой."""
        engine = self.create_engine()
        agent = Agent(Build(damage=3, health=7))

        with pytest.raises(ValueError, match="An agent cannot fight itself"):
            engine.start_battle(
                agent,
                agent,
                self.create_strategy(),
                self.create_strategy(),
            )
