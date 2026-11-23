import pytest

from metalab.action_rules.attack import AttackRules
from metalab.action_rules_registry import ActionRulesRegistry
from metalab.action_type import ActionType


class TestActionRegistry:
    def test_get_attack_rules(self):
        registry = ActionRulesRegistry()

        rules = registry.get(ActionType.ATTACK)

        assert isinstance(rules, AttackRules)

    def test_get_returns_same_instance(self):
        registry = ActionRulesRegistry()

        first_rules = registry.get(ActionType.ATTACK)
        second_rules = registry.get(ActionType.ATTACK)

        assert first_rules is second_rules

    def test_get_invalid_action_type(self):
        registry = ActionRulesRegistry()

        with pytest.raises(KeyError):
            registry.get("INVALID")
