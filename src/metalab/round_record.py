
from dataclasses import dataclass

from metalab.action import Action
from metalab.effect import Effect
from metalab.agent_snapshot import AgentSnapshot


@dataclass(frozen=True)
class RoundRecord:
    """Хранит данные одного завершённого раунда."""

    round_number: int

    agent_a_before: AgentSnapshot
    agent_b_before: AgentSnapshot

    action_a: Action
    action_b: Action

    effects_a: tuple[Effect, ...]
    effects_b: tuple[Effect, ...]

    agent_a_after: AgentSnapshot
    agent_b_after: AgentSnapshot

    def __post_init__(self) -> None:
        if not isinstance(self.round_number, int) or isinstance(
            self.round_number, bool
        ):
            raise TypeError("round_number must be an integer")

        if self.round_number < 1:
            raise ValueError("round_number must be greater than or equal to 1")

        snapshot_fields = (
            "agent_a_before",
            "agent_b_before",
            "agent_a_after",
            "agent_b_after",
        )

        for field_name in snapshot_fields:
            if not isinstance(getattr(self, field_name), AgentSnapshot):
                raise TypeError(f"{field_name} must be an AgentSnapshot")

        action_fields = ("action_a", "action_b")

        for field_name in action_fields:
            if not isinstance(getattr(self, field_name), Action):
                raise TypeError(f"{field_name} must be an Action")

        effects_fields = ("effects_a", "effects_b")

        for field_name in effects_fields:
            effects = getattr(self, field_name)

            if not isinstance(effects, tuple):
                raise TypeError(f"{field_name} must be a tuple")

            if not all(isinstance(effect, Effect) for effect in effects):
                raise TypeError(f"all items in {field_name} must be Effect instances")
