from enum import Enum, auto


class BattleOutcome(Enum):
    A_WON = auto()
    B_WON = auto()
    BOTH_LOST = auto()
    BOTH_WON = auto()