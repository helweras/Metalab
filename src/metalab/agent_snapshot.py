from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSnapshot:
    health: int
    damage: int

    def __post_init__(self):
        attributes = (self.health, self.damage)

        if any(type(attribute) is not int for attribute in attributes):
            raise TypeError("Attributes must be integers")