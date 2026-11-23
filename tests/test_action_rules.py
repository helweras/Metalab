import pytest

from metalab.action_rules.base import ActionRules


class TestActionRules:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            ActionRules()

    def test_cannot_instantiate_incomplete_subclass(self):
        class IncompleteRules(ActionRules):
            pass

        with pytest.raises(TypeError):
            IncompleteRules()

    def test_can_instantiate_complete_subclass(self):
        class CompleteRules(ActionRules):
            def calculate_effects(self, state, target):
                pass

        action_rules = CompleteRules()
        assert isinstance(action_rules, CompleteRules)
