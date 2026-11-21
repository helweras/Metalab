from metalab.agent import Agent
from metalab.agent_strategy import AgentStrategy
from metalab.battle_outcome import BattleOutcome
from metalab.battle_rules import BattleRules
from metalab.battle_settings import BattleSettings
from metalab.action_rules_registry import ActionRulesRegistry


class BattleEngine:
    def __init__(self,
                 agent_a: Agent,
                 agent_b: Agent,
                 strategy_a: AgentStrategy,
                 strategy_b: AgentStrategy,
                 action_rules: ActionRulesRegistry,
                 battle_rules: BattleRules) -> None:

        self.__agent_a = agent_a
        self.__agent_b = agent_b
        self.__strategy_a = strategy_a
        self.__strategy_b = strategy_b
        self.__action_rules = action_rules
        self.__battle_rules = battle_rules

    def start_battle(self):
        current_round = 1
        alive_a = self.__agent_a.is_alive
        alive_b = self.__agent_b.is_alive
        outcome = self.__battle_rules.determine_outcome(agent_a_alive=alive_a,
                                                 agent_b_alive=alive_b,
                                                 current_round=current_round)
        if outcome is None:
            snapshot_a = self.__agent_a.snapshot
            snapshot_b = self.__agent_b.snapshot




