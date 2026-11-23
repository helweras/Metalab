from metalab.target import Target


class TestTarget:
    def test_target_names(self):
        assert Target.ENEMY.name == "ENEMY"
        assert Target.SELF.name == "SELF"
