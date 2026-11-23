from dataclasses import FrozenInstanceError

import pytest

from metalab.action_result import ActionResult
from metalab.attribute import Attribute


class TestActionResult:
    def test_init(self):
        result = ActionResult(Attribute.HEALTH, 10)

        assert result.attribute == Attribute.HEALTH
        assert result.value == 10

    @pytest.mark.parametrize(
        "attribute, value",
        [
            ("HEALTH", 10),
            (Attribute.HEALTH, "10"),
            (Attribute.HEALTH, 5.7),
            (Attribute.HEALTH, True),
        ],
    )
    def test_init_invalid_types(self, attribute, value):
        with pytest.raises(TypeError):
            ActionResult(attribute, value)

    def test_immutable(self):
        result = ActionResult(Attribute.HEALTH, 10)

        with pytest.raises(FrozenInstanceError):
            result.attribute = Attribute.HEALTH

        with pytest.raises(FrozenInstanceError):
            result.value = 20
