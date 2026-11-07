from dataclasses import dataclass, astuple


@dataclass(frozen=True)
class Effect:
    damage: int

    def __post_init__(self):
        attributes = astuple(self)
        if any(type(a) is not int for a in attributes):
            raise TypeError("Attributes must be an integer")
