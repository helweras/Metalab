from dataclasses import dataclass
from enum import Enum, auto
from metalab.action_rules import ActionRules


class EffectTarget(Enum):
    SELF = auto()
    ENEMY = auto()
    BOTH = auto()


@dataclass(frozen=True)
class Effect:
    action_rule: ActionRules
    target: EffectTarget = EffectTarget.ENEMY

    def __post_init__(self):
        if not isinstance(self.action_rule, ActionRules):
            raise TypeError("action_rule must be an ActionRules")

        if not isinstance(self.target, EffectTarget):
            raise TypeError("Target must be an EffectTarget")

