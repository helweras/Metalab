from dataclasses import dataclass, astuple


@dataclass(frozen=True)
class AgentState:
    own_health: int
    own_damage: int
    enemy_health: int
    enemy_damage: int

    def __post_init__(self):

        attributes = astuple(self)
        if any(type(a) is not int for a in attributes):
            raise TypeError("AgentState attributes must be integers")

