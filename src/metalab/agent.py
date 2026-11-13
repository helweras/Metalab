from src.metalab.build import Build
from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute

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

    # def take_damage(self, damage):
    #     if type(damage) is not int:
    #         raise TypeError("Damage must be an integer")
    #     self.__current_health -= damage

    @property
    def state(self) -> AgentSnapshot:
        return AgentSnapshot(
            health=self.__current_health,
            damage=self.__current_damage
        )