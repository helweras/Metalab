from dataclasses import dataclass

from metalab.action_result import ActionResult
from metalab.target import Target


@dataclass(frozen=True)
class Effect:
    action_result: ActionResult
    target: Target = Target.ENEMY

    def __post_init__(self):
        if not isinstance(self.action_result, ActionResult):
            raise TypeError("action_result must be an ActionResult")

        if not isinstance(self.target, Target):
            raise TypeError("Target must be a Target")
