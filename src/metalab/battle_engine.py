
from metalab.agent import Agent
from metalab.agent_strategy import AgentStrategy
from metalab.battle_rules import BattleRules
from metalab.agent_perspective import AgentPerspective
from metalab.action_rules_registry import ActionRulesRegistry
from metalab.effect import Effect
from metalab.target import Target
from metalab.battle_result import BattleResult


class BattleEngine:
    def __init__(
        self,
        action_rules: ActionRulesRegistry,
        battle_rules: BattleRules,
    ) -> None:
        # Правила исполнения действий и определения исхода боя.
        # Не зависят от конкретных участников и могут использоваться
        # при проведении нескольких боёв.
        self.__action_rules = action_rules
        self.__battle_rules = battle_rules

    def apply_effects(
        self,
        source_agent: Agent,
        target_agent: Agent,
        effects: tuple[Effect, ...],
    ) -> None:
        # Применяет рассчитанные эффекты к соответствующим агентам.
        # SELF — сам агент, выполнивший действие.
        # ENEMY — его противник.
        for effect in effects:
            if effect.target == Target.SELF:
                recipient = source_agent
            elif effect.target == Target.ENEMY:
                recipient = target_agent
            else:
                raise ValueError("Unknown effect target")

            recipient.apply_action_result(effect.action_result)

    def start_battle(
        self,
        agent_a: Agent,
        agent_b: Agent,
        strategy_a: AgentStrategy,
        strategy_b: AgentStrategy,
    ) -> BattleResult:

        if agent_a is agent_b:
            raise ValueError("An agent cannot fight itself")
        # Счётчик начинается с нуля и увеличивается после каждого раунда.
        current_round = 0

        # Проверяем начальное состояние участников.
        alive_a = agent_a.is_alive
        alive_b = agent_b.is_alive

        outcome = self.__battle_rules.determine_outcome(
            agent_a_alive=alive_a,
            agent_b_alive=alive_b,
            current_round=current_round,
        )

        # Раунды выполняются, пока правила боя не определят его исход.
        while outcome is None:
            # Создаём снимки состояния обоих агентов в начале раунда.
            # Оба участника будут принимать решения на основе одного и того же состояния боя.
            snapshot_a = agent_a.snapshot
            snapshot_b = agent_b.snapshot

            # Формируем перспективы участников:
            # каждый агент видит собственное состояние и состояние противника.
            a_perspective = AgentPerspective(
                own_state=snapshot_a,
                enemy_state=snapshot_b,
            )
            b_perspective = AgentPerspective(
                own_state=snapshot_b,
                enemy_state=snapshot_a,
            )

            # Обе стратегии выбирают действия до применения эффектов.
            action_a = strategy_a.choose_action(a_perspective)
            action_b = strategy_b.choose_action(b_perspective)

            # Получаем правила исполнения выбранных действий.
            action_rule_a = self.__action_rules.get(action_a.action_type)
            action_rule_b = self.__action_rules.get(action_b.action_type)

            # Рассчитываем эффекты обоих действий на основе начального
            # состояния раунда. На этом этапе характеристики не изменяются.
            effects_tuple_a = action_rule_a.calculate_effects(
                a_perspective,
                action_a.target,
            )
            effects_tuple_b = action_rule_b.calculate_effects(
                b_perspective,
                action_b.target,
            )

            # Применяем эффекты первого участника.
            self.apply_effects(
                source_agent=agent_a,
                target_agent=agent_b,
                effects=effects_tuple_a,
            )

            # Применяем эффекты второго участника.
            # Даже если первый участник уничтожил второго,
            # уже выбранное действие второго всё равно выполняется.
            self.apply_effects(
                source_agent=agent_b,
                target_agent=agent_a,
                effects=effects_tuple_b,
            )

            # Раунд считается завершённым после применения всех эффектов.
            current_round += 1

            # Проверяем актуальное состояние участников после раунда.
            alive_a = agent_a.is_alive
            alive_b = agent_b.is_alive

            # Определяем, завершился ли бой:
            # по смерти участников или достижению максимального числа раундов.
            outcome = self.__battle_rules.determine_outcome(
                agent_a_alive=alive_a,
                agent_b_alive=alive_b,
                current_round=current_round,
            )

        # Возвращаем результат боя с итоговым состоянием обоих участников.
        return BattleResult(
            outcome=outcome,
            rounds_played=current_round,
            agent_a_state=agent_a.snapshot,
            agent_b_state=agent_b.snapshot,
        )
