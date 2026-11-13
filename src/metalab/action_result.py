from dataclasses import dataclass


@dataclass(frozen=True)
class ActionResult:
    attribute: Attribute
    value: int