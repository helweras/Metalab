
from metalab.action_type import ActionType
from metalab.action_rules.base import ActionRules
from metalab.action_rules.attack import AttackRules


class ActionRulesRegistry:
    def __init__(self) -> None:
        self.__rules: dict[ActionType, ActionRules] = {
            ActionType.ATTACK: AttackRules(),
        }

    def get(self, action_type: ActionType) -> ActionRules:
        return self.__rules[action_type]
