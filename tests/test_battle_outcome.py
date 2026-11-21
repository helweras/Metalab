from metalab.battle_outcome import BattleOutcome


class TestBattleOutcome:
    def test_members(self):
        assert set(BattleOutcome) == {
            BattleOutcome.A_WON,
            BattleOutcome.B_WON,
            BattleOutcome.BOTH_LOST,
            BattleOutcome.BOTH_WON,
        }

    def test_members_count(self):
        assert len(BattleOutcome) == 4

    def test_members_are_unique(self):
        assert len(set(BattleOutcome)) == 4