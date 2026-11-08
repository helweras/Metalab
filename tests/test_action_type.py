from metalab.action_type import ActionType

class TestActionType:
    def test_attack(self):
        assert ActionType.ATTACK.name == "ATTACK"