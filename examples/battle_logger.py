from metalab.action import Action
from metalab.agent_snapshot import AgentSnapshot
from metalab.battle_result import BattleResult
from metalab.effect import Effect


class BattleLogger:
    """Выводит этапы боя и изменения состояния агентов в консоль."""

    @staticmethod
    def _format_state(state: AgentSnapshot) -> str:
        attributes = ", ".join(
            f"{attribute.name.lower()}={value}"
            for attribute, value in state.attributes.items()
        )
        return f"{{{attributes}}}"

    @staticmethod
    def _format_action(action: Action) -> str:
        return f"{action.action_type.name} -> {action.target.name}"

    @staticmethod
    def _format_effects(effects: tuple[Effect, ...]) -> str:
        if not effects:
            return "нет эффектов"

        return "; ".join(
            (
                f"{effect.target.name}: "
                f"{effect.action_result.attribute.name} "
                f"{effect.action_result.value:+}"
            )
            for effect in effects
        )

    def on_battle_start(
        self,
        agent_a_state: AgentSnapshot,
        agent_b_state: AgentSnapshot,
    ) -> None:
        print("=== НАЧАЛО БОЯ ===")
        print(f"Агент A: {self._format_state(agent_a_state)}")
        print(f"Агент B: {self._format_state(agent_b_state)}")

    def on_round_start(
        self,
        round_number: int,
        agent_a_state: AgentSnapshot,
        agent_b_state: AgentSnapshot,
    ) -> None:
        print(f"\n=== РАУНД {round_number} ===")
        print(f"Состояние A: {self._format_state(agent_a_state)}")
        print(f"Состояние B: {self._format_state(agent_b_state)}")

    def on_actions_selected(
        self,
        round_number: int,
        action_a: Action,
        action_b: Action,
    ) -> None:
        print(f"Выбор действий: A — {self._format_action(action_a)}")
        print(f"                 B — {self._format_action(action_b)}")

    def on_effects_calculated(
        self,
        round_number: int,
        effects_a: tuple[Effect, ...],
        effects_b: tuple[Effect, ...],
    ) -> None:
        print(f"Рассчитанные эффекты A: {self._format_effects(effects_a)}")
        print(f"Рассчитанные эффекты B: {self._format_effects(effects_b)}")

    def on_effects_applied(
        self,
        round_number: int,
        source: str,
        agent_a_state: AgentSnapshot,
        agent_b_state: AgentSnapshot,
    ) -> None:
        print(f"После применения эффектов агента {source}:")
        print(f"  Агент A: {self._format_state(agent_a_state)}")
        print(f"  Агент B: {self._format_state(agent_b_state)}")

    def on_round_end(
        self,
        round_number: int,
        agent_a_alive: bool,
        agent_b_alive: bool,
    ) -> None:
        print(
            f"Конец раунда {round_number}: "
            f"A {'жив' if agent_a_alive else 'погиб'}, "
            f"B {'жив' if agent_b_alive else 'погиб'}"
        )

    def on_battle_end(self, result: BattleResult) -> None:
        print("\n=== БОЙ ЗАВЕРШЁН ===")
        print(f"Исход: {result.outcome.name}")
        print(f"Раундов проведено: {result.rounds_played}")
        print(f"Итог A: {self._format_state(result.agent_a_state)}")
        print(f"Итог B: {self._format_state(result.agent_b_state)}")
