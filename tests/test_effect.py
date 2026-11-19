import pytest
from dataclasses import FrozenInstanceError

from metalab.effect import Effect
from metalab.action_result import ActionResult
from metalab.attribute import Attribute
from metalab.target import Target


class TestEffect:
    @pytest.mark.parametrize(
        "action_result, target",
        [
            (ActionResult(Attribute.HEALTH, 10), Target.ENEMY),
            (ActionResult(Attribute.DAMAGE, 5), Target.SELF),
            (ActionResult(Attribute.HEALTH, 0), Target.ENEMY),
        ],
    )
    def test_init(self, action_result, target):
        effect = Effect(action_result, target)

        assert effect.action_result == action_result
        assert effect.target == target

    def test_init_default_target(self):
        action_result = ActionResult(Attribute.HEALTH, 10)

        effect = Effect(action_result)

        assert effect.action_result == action_result
        assert effect.target == Target.ENEMY

    @pytest.mark.parametrize(
        "action_result, target",
        [
            ("INVALID", Target.ENEMY),
            (ActionResult(Attribute.HEALTH, 10), "ENEMY"),
        ],
    )
    def test_init_invalid_types(self, action_result, target):
        with pytest.raises(TypeError):
            Effect(action_result, target)

    def test_immutable(self):
        effect = Effect(
            ActionResult(Attribute.HEALTH, 10),
            Target.ENEMY,
        )

        with pytest.raises(FrozenInstanceError):
            effect.action_result = ActionResult(Attribute.DAMAGE, 5)

        with pytest.raises(FrozenInstanceError):
            effect.target = Target.SELF
