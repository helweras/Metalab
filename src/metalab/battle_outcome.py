from enum import Enum, auto


class BattleOutcome(Enum):
    A_WON = auto()
    B_WON = auto()
    DRAW = auto()
    BOTH_WON = auto()