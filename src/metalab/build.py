from dataclasses import astuple, dataclass

from metalab.const.build_const import MAX_BUILD_POINTS


@dataclass(frozen=True)
class Build:
    damage: int
    health: int

    def __post_init__(self):

        attributes = astuple(self)
        if any(type(a) is not int for a in attributes):
            raise TypeError("Attributes must be an integer")
        if sum(attributes) > MAX_BUILD_POINTS:
            raise ValueError("Build exceeds the maximum attribute points")
        if any(atr <= 0 for atr in attributes):
            raise ValueError("Attributes must be greater than zero")
