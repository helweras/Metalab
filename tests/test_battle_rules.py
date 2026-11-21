
import pytest

from metalab.battle_outcome import BattleOutcome
from metalab.battle_rules import BattleRules
from metalab.battle_settings import BattleSettings


class TestBattleRules:
    @pytest.mark.parametrize(
        "agent_a_alive, agent_b_alive, current_round, expected",
        [
            (False, False, 1, BattleOutcome.BOTH_LOST),
            (False, True, 1, BattleOutcome.B_WON),
            (True, False, 1, BattleOutcome.A_WON),
            (True, True, 1, None),
            (True, True, 4, None),
            (True, True, 5, BattleOutcome.BOTH_WON),
            (True, True, 6, BattleOutcome.BOTH_WON),
        ],
    )
    def test_determine_outcome(
        self,
        agent_a_alive,
        agent_b_alive,
        current_round,
        expected,
    ):
        rules = BattleRules(BattleSettings(max_rounds=5))

        outcome = rules.determine_outcome(
            agent_a_alive,
            agent_b_alive,
            current_round,
        )

        assert outcome == expected

    @pytest.mark.parametrize(
        "agent_a_alive, agent_b_alive, current_round",
        [
            ("True", True, 1),
            (1, True, 1),
            (None, True, 1),
            (True, "False", 1),
            (True, 0, 1),
            (True, None, 1),
            (True, True, "1"),
            (True, True, 1.5),
            (True, True, True),
            (True, True, None),
        ],
    )
    def test_determine_outcome_invalid_types(
        self,
        agent_a_alive,
        agent_b_alive,
        current_round,
    ):
        rules = BattleRules(BattleSettings(max_rounds=5))

        with pytest.raises(TypeError):
            rules.determine_outcome(
                agent_a_alive,
                agent_b_alive,
                current_round,
            )

    @pytest.mark.parametrize("current_round", [0, -1, -5])
    def test_determine_outcome_invalid_round(
        self,
        current_round,
    ):
        rules = BattleRules(BattleSettings(max_rounds=5))

        with pytest.raises(ValueError):
            rules.determine_outcome(
                True,
                True,
                current_round,
            )

    @pytest.mark.parametrize(
        "settings",
        [
            None,
            5,
            "settings",
        ],
    )
    def test_init_invalid_settings(self, settings):
        with pytest.raises(TypeError):
            BattleRules(settings)
