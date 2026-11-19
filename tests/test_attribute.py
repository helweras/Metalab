from enum import Enum

from metalab.attribute import Attribute


class TestAttribute:
    def test_members(self):
        assert list(Attribute) == [
            Attribute.HEALTH,
            Attribute.DAMAGE,
        ]

    def test_is_enum(self):
        assert issubclass(Attribute, Enum)

    def test_members_are_unique(self):
        assert len(Attribute) == len(set(Attribute))
