from metalab.attack import Attack
from dataclasses import dataclass

@dataclass(frozen=True)
class ActionRegistry:
    attack: Attack
