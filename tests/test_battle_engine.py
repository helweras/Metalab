
import pytest

from metalab.action_result import ActionResult
from metalab.action_rules_registry import ActionRulesRegistry
from metalab.agent import Agent
from metalab.agent_strategy import AgentStrategy
from metalab.attribute import Attribute
from metalab.battle_engine import BattleEngine
from metalab.battle_outcome import BattleOutcome
from metalab.battle_rules import BattleRules
from metalab.battle_settings import BattleSettings
from metalab.build import Build
from metalab.const.action_const import AVAILABLE_ACTIONS
from metalab.effect import Effect
from metalab.target import Target


class TestBattleEngine:
    """Тесты применения эффектов и выполнения боевых сценариев."""

    @staticmethod
    def create_engine(max_rounds=5):
        """Создаёт боевой движок с заданным ограничением раундов."""
        return BattleEngine(
            action_rules=ActionRulesRegistry(),
            battle_rules=BattleRules(BattleSettings(max_rounds)),
        )

    @staticmethod
    def create_strategy():
        """Создаёт стратегию со всеми доступными действиями."""
        return AgentStrategy(AVAILABLE_ACTIONS)

    @staticmethod
    def create_agent(damage=5, health=7):
        """Создаёт агента с заданными характеристиками."""
        return Agent(Build(damage=damage, health=health))

    # Инициализация движка

    def test_init(self):
        """Проверяет успешное создание боевого движка."""
        engine = self.create_engine()

        assert isinstance(engine, BattleEngine)

    @pytest.mark.parametrize(
        "action_rules",
        [None, {}, [], "rules", 1, True],
    )
    def test_init_invalid_action_rules(self, action_rules):
        """Проверяет отклонение некорректного реестра правил действий."""
        with pytest.raises(TypeError):
            BattleEngine(
                action_rules=action_rules,
                battle_rules=BattleRules(BattleSettings(5)),
            )

    @pytest.mark.parametrize(
        "battle_rules",
        [None, {}, [], "rules", 1, True],
    )
    def test_init_invalid_battle_rules(self, battle_rules):
        """Проверяет отклонение некорректных правил боя."""
        with pytest.raises(TypeError):
            BattleEngine(
                action_rules=ActionRulesRegistry(),
                battle_rules=battle_rules,
            )

    # Применение эффектов

    def test_apply_effects_to_self(self):
        """Проверяет применение эффекта к самому источнику."""
        engine = self.create_engine()
        agent = self.create_agent(health=6)
        enemy = self.create_agent(damage=3, health=8)

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
        agent = self.create_agent(health=6)
        enemy = self.create_agent(damage=3, health=8)

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
        agent = self.create_agent(health=6)
        enemy = self.create_agent(damage=3, health=8)

        effects = (
            Effect(ActionResult(Attribute.HEALTH, -2), Target.SELF),
            Effect(ActionResult(Attribute.HEALTH, -3), Target.ENEMY),
            Effect(ActionResult(Attribute.HEALTH, -1), Target.SELF),
        )

        engine.apply_effects(agent, enemy, effects)

        assert agent.snapshot.attributes[Attribute.HEALTH] == 3
        assert enemy.snapshot.attributes[Attribute.HEALTH] == 5

    def test_apply_empty_effects(self):
        """Проверяет обработку пустого набора эффектов."""
        engine = self.create_engine()
        agent = self.create_agent(health=6)
        enemy = self.create_agent(damage=3, health=8)

        engine.apply_effects(agent, enemy, ())

        assert agent.snapshot.attributes[Attribute.HEALTH] == 6
        assert enemy.snapshot.attributes[Attribute.HEALTH] == 8

    @pytest.mark.parametrize(
        "source_agent",
        [None, {}, [], "agent", 1, True],
    )
    def test_apply_effects_invalid_source_agent(self, source_agent):
        """Проверяет отклонение некорректного исходного агента."""
        engine = self.create_engine()
        enemy = self.create_agent()

        with pytest.raises(TypeError):
            engine.apply_effects(source_agent, enemy, ())

    @pytest.mark.parametrize(
        "target_agent",
        [None, {}, [], "agent", 1, True],
    )
    def test_apply_effects_invalid_target_agent(self, target_agent):
        """Проверяет отклонение некорректного целевого агента."""
        engine = self.create_engine()
        agent = self.create_agent()

        with pytest.raises(TypeError):
            engine.apply_effects(agent, target_agent, ())

    @pytest.mark.parametrize(
        "effects",
        [None, [], {}, "effects", 1, True],
    )
    def test_apply_effects_invalid_effects_type(self, effects):
        """Проверяет отклонение некорректного типа effects."""
        engine = self.create_engine()
        agent = self.create_agent()
        enemy = self.create_agent()

        with pytest.raises(TypeError):
            engine.apply_effects(agent, enemy, effects)

    def test_apply_effects_invalid_effect_item(self):
        """Проверяет отклонение элементов, не являющихся эффектами."""
        engine = self.create_engine()
        agent = self.create_agent()
        enemy = self.create_agent()

        with pytest.raises(TypeError):
            engine.apply_effects(agent, enemy, (object(),))

    # Выполнение боя

    def test_start_battle_both_agents_survive_max_rounds(self):
        """Проверяет завершение боя по достижении лимита раундов."""
        engine = self.create_engine(max_rounds=1)

        agent_a = self.create_agent(damage=3, health=8)
        agent_b = self.create_agent(damage=4, health=7)

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
        assert len(result.history) == 1

    def test_start_battle_applies_second_action_after_agent_b_dies(self):
        """Проверяет применение обоих действий при смертельной атаке."""
        engine = self.create_engine()

        agent_a = self.create_agent(damage=6, health=6)
        agent_b = self.create_agent(damage=6, health=6)

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
        assert len(result.history) == 1

    def test_start_battle_agent_a_loses(self):
        """Проверяет победу агента B при гибели агента A."""
        engine = self.create_engine()

        agent_a = self.create_agent(damage=2, health=8)
        agent_b = self.create_agent(damage=8, health=3)

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

        agent_a = self.create_agent(damage=8, health=3)
        agent_b = self.create_agent(damage=2, health=8)

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

    def test_start_battle_agents_cannot_fight_itself(self):
        """Проверяет запрет боя агента с самим собой."""
        engine = self.create_engine()
        agent = self.create_agent(damage=3, health=7)

        with pytest.raises(
            ValueError,
            match="An agent cannot fight itself",
        ):
            engine.start_battle(
                agent,
                agent,
                self.create_strategy(),
                self.create_strategy(),
            )

    # Проверка входных условий

    @pytest.mark.parametrize(
        "agent_a",
        [None, {}, [], "agent", 1, True],
    )
    def test_start_battle_invalid_agent_a(self, agent_a):
        """Проверяет отклонение некорректного первого агента."""
        engine = self.create_engine()

        with pytest.raises(TypeError):
            engine.start_battle(
                agent_a,
                self.create_agent(),
                self.create_strategy(),
                self.create_strategy(),
            )

    @pytest.mark.parametrize(
        "agent_b",
        [None, {}, [], "agent", 1, True],
    )
    def test_start_battle_invalid_agent_b(self, agent_b):
        """Проверяет отклонение некорректного второго агента."""
        engine = self.create_engine()

        with pytest.raises(TypeError):
            engine.start_battle(
                self.create_agent(),
                agent_b,
                self.create_strategy(),
                self.create_strategy(),
            )

    @pytest.mark.parametrize(
        "strategy_a",
        [None, {}, [], "strategy", 1, True],
    )
    def test_start_battle_invalid_strategy_a(self, strategy_a):
        """Проверяет отклонение некорректной первой стратегии."""
        engine = self.create_engine()

        with pytest.raises(TypeError):
            engine.start_battle(
                self.create_agent(),
                self.create_agent(),
                strategy_a,
                self.create_strategy(),
            )

    @pytest.mark.parametrize(
        "strategy_b",
        [None, {}, [], "strategy", 1, True],
    )
    def test_start_battle_invalid_strategy_b(self, strategy_b):
        """Проверяет отклонение некорректной второй стратегии."""
        engine = self.create_engine()

        with pytest.raises(TypeError):
            engine.start_battle(
                self.create_agent(),
                self.create_agent(),
                self.create_strategy(),
                strategy_b,
            )
