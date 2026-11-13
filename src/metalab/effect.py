from dataclasses import dataclass
from metalab.target import Target
from metalab.action_result import ActionResult




@dataclass(frozen=True)
class Effect:
    action_result: ActionResult
    target: Target = Target.ENEMY

    def __post_init__(self):
        if not isinstance(self.action_result, ActionResult):
            raise TypeError("action_rule must be an ActionResult")

        if not isinstance(self.target, Target):
            raise TypeError("Target must be an Target")

