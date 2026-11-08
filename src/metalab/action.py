from dataclasses import dataclass
from metalab.action_type import ActionType
from metalab.target import Target


@dataclass(frozen=True)
class Action:
   action_type: ActionType
   target: Target

   def __post_init__(self):
       if not isinstance(self.action_type, ActionType):
           raise TypeError(f'{self.action_type} is not an ActionType')
       if not isinstance(self.target, Target):
           raise TypeError(f'{self.target} is not a Target')