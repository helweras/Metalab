import pytest
from src.metalab.build import Build
from contextlib import nullcontext as does_not_raise
from dataclasses import FrozenInstanceError


class TestBuild:
    @pytest.mark.parametrize("damage, health, expectation",
                             [
                                 (6, 4, does_not_raise()),
                                 (6, 6, does_not_raise()),
                                 (0, 11, pytest.raises(ValueError)),
                                 (-1, 12, pytest.raises(ValueError)),
                                 (3.5, 8, pytest.raises(TypeError)),
                                 (7, "4", pytest.raises(TypeError)),
                                 (True, 10, pytest.raises(TypeError)),
                                 (7, 6, pytest.raises(ValueError)),
                             ])
    def test_build(self, damage, health, expectation):
        with expectation:
            build = Build(damage, health)
            assert build.damage == damage
            assert build.health == health

    def test_build_immutable(self):
        build = Build(damage=5, health=6)
        with pytest.raises(FrozenInstanceError):
            build.damage = 10
