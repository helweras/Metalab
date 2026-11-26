from metalab.action_rules_registry import ActionRulesRegistry
from metalab.agent import Agent
from metalab.agent_perspective import AgentPerspective
from metalab.agent_strategy import AgentStrategy
from metalab.battle_history import BattleHistory
from metalab.battle_result import BattleResult
from metalab.battle_rules import BattleRules
from metalab.effect import Effect
from metalab.round_record import RoundRecord
from metalab.target import Target


class BattleEngine:
    def __init__(
            self,
            action_rules: ActionRulesRegistry,
            battle_rules: BattleRules,
    ) -> None:
        if not isinstance(action_rules, ActionRulesRegistry):
            raise TypeError("action_rules must be an ActionRulesRegistry")

        if not isinstance(battle_rules, BattleRules):
            raise TypeError("battle_rules must be a BattleRules")

        self.__action_rules = action_rules
        self.__battle_rules = battle_rules
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
        if not isinstance(source_agent, Agent):
            raise TypeError("source_agent must be an Agent")

        if not isinstance(target_agent, Agent):
            raise TypeError("target_agent must be an Agent")

        if not isinstance(effects, tuple):
            raise TypeError("effects must be a tuple")

        if not all(isinstance(effect, Effect) for effect in effects):
            raise TypeError("all effects must be Effect instances")

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

        if not isinstance(agent_a, Agent):
            raise TypeError("agent_a must be an Agent")

        if not isinstance(agent_b, Agent):
            raise TypeError("agent_b must be an Agent")

        if not isinstance(strategy_a, AgentStrategy):
            raise TypeError("strategy_a must be an AgentStrategy")

        if not isinstance(strategy_b, AgentStrategy):
            raise TypeError("strategy_b must be an AgentStrategy")

        if agent_a is agent_b:
            raise ValueError("An agent cannot fight itself")

        round_records: list[RoundRecord] = []
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
            # Оба участника будут принимать решения
            # на основе одного и того же состояния боя.
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

            # Сохраняем состояние обоих участников после завершения раунда.
            snapshot_a_after = agent_a.snapshot
            snapshot_b_after = agent_b.snapshot

            # Создаём запись завершённого раунда.
            round_records.append(
                RoundRecord(
                    round_number=current_round,
                    agent_a_before=snapshot_a,
                    agent_b_before=snapshot_b,
                    action_a=action_a,
                    action_b=action_b,
                    effects_a=effects_tuple_a,
                    effects_b=effects_tuple_b,
                    agent_a_after=snapshot_a_after,
                    agent_b_after=snapshot_b_after,
                )
            )

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
            history=BattleHistory(rounds=tuple(round_records))
        )
