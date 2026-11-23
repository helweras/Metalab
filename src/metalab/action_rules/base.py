from abc import ABC, abstractmethod

from metalab.agent_perspective import AgentPerspective
from metalab.effect import Effect
from metalab.target import Target


class ActionRules(ABC):
    @abstractmethod
    def calculate_effects(
        self, state: AgentPerspective, target: Target
    ) -> tuple[Effect, ...]:
        pass
