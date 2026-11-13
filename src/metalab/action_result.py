from dataclasses import dataclass
from metalab.attribute import Attribute


@dataclass(frozen=True)
class ActionResult:
    attribute: Attribute
    value: int