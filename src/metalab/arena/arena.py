from metalab.agent import Agent
from metalab.battle_engine import BattleEngine
from metalab.battle_history_formatter import BattleHistoryFormatter
from metalab.build import Build
from metalab.action_rules_registry import ActionRulesRegistry
from metalab.battle_rules import BattleRules
from metalab.battle_settings import BattleSettings
from metalab.agent_strategy import AgentStrategy
from metalab.const.action_const import AVAILABLE_ACTIONS

build_a = Build(
    damage=1,
    health=7,
)

build_b = Build(
    damage=1,
    health=5,
)

agent_a = Agent(build_a)
agent_b = Agent(build_b)


strategy_a = AgentStrategy(AVAILABLE_ACTIONS)
strategy_b = AgentStrategy(AVAILABLE_ACTIONS)


engine = BattleEngine(
    action_rules=ActionRulesRegistry(),
    battle_rules=BattleRules(BattleSettings(max_rounds=10))
)

result = engine.start_battle(
    agent_a=agent_a,
    agent_b=agent_b,
    strategy_a=strategy_a,
    strategy_b=strategy_b,
)
formatter = BattleHistoryFormatter()
print(formatter.format(result))