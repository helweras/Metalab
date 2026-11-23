from dataclasses import dataclass

from metalab.attribute import Attribute


@dataclass(frozen=True)
class ActionResult:
    attribute: Attribute
    value: int

    def __post_init__(self):
        if not isinstance(self.attribute, Attribute):
            raise TypeError("attribute must be an Attribute")

        if type(self.value) is not int:
            raise TypeError("value must be an int")
