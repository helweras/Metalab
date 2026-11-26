
from dataclasses import dataclass

from metalab.agent_snapshot import AgentSnapshot
from metalab.battle_outcome import BattleOutcome
from metalab.battle_history import BattleHistory


@dataclass(frozen=True)
class BattleResult:
    outcome: BattleOutcome
    rounds_played: int
    agent_a_state: AgentSnapshot
    agent_b_state: AgentSnapshot
    history: BattleHistory

    def __post_init__(self):
        if not isinstance(self.outcome, BattleOutcome):
            raise TypeError("outcome must be a BattleOutcome")

        if type(self.rounds_played) is not int:
            raise TypeError("rounds_played must be an integer")

        if self.rounds_played < 0:
            raise ValueError("rounds_played must be non-negative")

        if not isinstance(self.agent_a_state, AgentSnapshot):
            raise TypeError("agent_a_state must be an AgentSnapshot")

        if not isinstance(self.agent_b_state, AgentSnapshot):
            raise TypeError("agent_b_state must be an AgentSnapshot")

        if not isinstance(self.history, BattleHistory):
            raise TypeError("history must be a BattleHistory")
