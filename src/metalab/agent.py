from metalab.build import Build
from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute
from metalab.action_result import ActionResult

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
        return AgentSnapshot(
            self.__current_attributes
        )

    def apply_action_result(self, result: ActionResult) -> None:
        self.__current_attributes[result.attribute] += result.value