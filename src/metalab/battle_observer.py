from typing import Protocol

from metalab.action import Action
from metalab.agent_snapshot import AgentSnapshot
from metalab.battle_result import BattleResult
from metalab.effect import Effect


class BattleObserver(Protocol):
    """Интерфейс наблюдателя за ходом боя."""

    def on_battle_start(
        self,
        agent_a_state: AgentSnapshot,
        agent_b_state: AgentSnapshot,
    ) -> None:
        ...

    def on_round_start(
        self,
        round_number: int,
        agent_a_state: AgentSnapshot,
        agent_b_state: AgentSnapshot,
    ) -> None:
        ...

    def on_actions_selected(
        self,
        round_number: int,
        action_a: Action,
        action_b: Action,
    ) -> None:
        ...

    def on_effects_calculated(
        self,
        round_number: int,
        effects_a: tuple[Effect, ...],
        effects_b: tuple[Effect, ...],
    ) -> None:
        ...

    def on_effects_applied(
        self,
        round_number: int,
        source: str,
        agent_a_state: AgentSnapshot,
        agent_b_state: AgentSnapshot,
    ) -> None:
        ...

    def on_round_end(
        self,
        round_number: int,
        agent_a_alive: bool,
        agent_b_alive: bool,
    ) -> None:
        ...

    def on_battle_end(self, result: BattleResult) -> None:
        ...
