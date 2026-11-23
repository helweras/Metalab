from dataclasses import FrozenInstanceError

import pytest

from metalab.battle_settings import BattleSettings


class TestBattleSettings:
    @pytest.mark.parametrize("max_rounds", [1, 2, 10, 100])
    def test_init(self, max_rounds):
        settings = BattleSettings(max_rounds)

        assert settings.max_rounds == max_rounds

    @pytest.mark.parametrize(
        "max_rounds",
        ["5", 5.5, True, None, [5]],
    )
    def test_init_invalid_type(self, max_rounds):
        with pytest.raises(TypeError):
            BattleSettings(max_rounds)

    @pytest.mark.parametrize("max_rounds", [0, -1, -10])
    def test_init_invalid_value(self, max_rounds):
        with pytest.raises(ValueError):
            BattleSettings(max_rounds)

    def test_immutable(self):
        settings = BattleSettings(10)

        with pytest.raises(FrozenInstanceError):
            settings.max_rounds = 20
