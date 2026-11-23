from metalab.action_result import ActionResult
from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute
from metalab.build import Build


class Agent:
    def __init__(self, build: Build):
        self.build = build
        self.__current_attributes = {
            Attribute.HEALTH: build.health,
            Attribute.DAMAGE: build.damage,
        }

    @property
    def is_alive(self):
        current_health = self.__current_attributes[Attribute.HEALTH]
        return current_health > 0

    @property
    def snapshot(self) -> AgentSnapshot:
        return AgentSnapshot(self.__current_attributes)

    def apply_action_result(self, action_result: ActionResult) -> None:
        if not isinstance(action_result, ActionResult):
            raise TypeError("action_result must be an ActionResult")
        attribute = action_result.attribute
        value = action_result.value

        current_value = self.__current_attributes[attribute]
        new_value = current_value + value

        if attribute == Attribute.HEALTH:
            max_value = self.build.health
            new_value = min(new_value, max_value)

        self.__current_attributes[attribute] = new_value
