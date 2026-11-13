from enum import Enum, auto

class EffectTarget(Enum):
    SELF = auto()
    ENEMY = auto()
    BOTH = auto()