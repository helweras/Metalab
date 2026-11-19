import pytest

from metalab.action_type import ActionType
from metalab.action_rules.attack import AttackRules
from metalab.action_registry import ActionRegistry


class TestActionRegistry:
    def test_get_attack_rules(self):
        registry = ActionRegistry()

        rules = registry.get(ActionType.ATTACK)

        assert isinstance(rules, AttackRules)

    def test_get_returns_same_instance(self):
        registry = ActionRegistry()

        first_rules = registry.get(ActionType.ATTACK)
        second_rules = registry.get(ActionType.ATTACK)

        assert first_rules is second_rules

    def test_get_invalid_action_type(self):
        registry = ActionRegistry()

        with pytest.raises(KeyError):
            registry.get("INVALID")
