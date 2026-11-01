from dataclasses import dataclass, astuple
from metalab.build_const import MAX_BUILD_POINTS


@dataclass(frozen=True)
class Build:
    damage: int
    health: int

    def __post_init__(self):
        attributes = astuple(self)
        if sum(attributes) > MAX_BUILD_POINTS:
            raise ValueError("Build exceeds the maximum attribute points")
        if any(atr <= 0 for atr in attributes):
            raise ValueError(f"atr must be greater than 0")

