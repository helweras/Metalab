from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from metalab.attribute import Attribute


@dataclass(frozen=True)
class AgentSnapshot:
    attributes: Mapping[Attribute, int]

    def __post_init__(self):
        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes))
        )