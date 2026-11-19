from dataclasses import dataclass


@dataclass(frozen=True)
class BattleSettings:
    max_rounds: int

    def __post_init__(self) -> None:
        if type(self.max_rounds) is not int:
            raise TypeError("max_rounds must be an integer")

        if self.max_rounds <= 0:
            raise ValueError("max_rounds must be positive")