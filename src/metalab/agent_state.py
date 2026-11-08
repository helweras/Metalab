from dataclasses import dataclass
from metalab.agent_snapshot import AgentSnapshot


@dataclass(frozen=True)
class AgentState:
    own_state: AgentSnapshot
    enemy_state: AgentSnapshot

    def __post_init__(self):
        if not isinstance(self.own_state, AgentSnapshot):
            raise TypeError("own_state must be an AgentSnapshot")

        if not isinstance(self.enemy_state, AgentSnapshot):
            raise TypeError("enemy_state must be an AgentSnapshot")

