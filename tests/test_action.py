from metalab.action import Action
from metalab.action_type import ActionType
from metalab.target import Target
from contextlib import nullcontext as does_not_raise
import pytest
from dataclasses import FrozenInstanceError


class TestAction:
    @pytest.mark.parametrize(
        "action_type, target, expectation",
        [
            (ActionType.ATTACK, Target.ENEMY, does_not_raise()),
            (ActionType.ATTACK, Target.SELF, does_not_raise()),
            (ActionType.ATTACK, "SELF", pytest.raises(TypeError)),
            ("ATTACK", Target.ENEMY, pytest.raises(TypeError)),
        ]
    )
    def test_init(self, action_type, target, expectation):
        with expectation:
            action = Action(action_type, target)
            assert action.target == target
            assert action.action_type == action_type

    def test_immutable(self):
        action = Action(ActionType.ATTACK, Target.ENEMY)

        with pytest.raises(FrozenInstanceError):
            action.target = Target.SELF

        with pytest.raises(FrozenInstanceError):
            action.action_type = ActionType.ATTACK
