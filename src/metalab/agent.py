from src.metalab.build import Build
from metalab.agent_snapshot import AgentSnapshot

class Agent:
    def __init__(self, build: Build):
        self.build = build
        self.__current_damage = self.build.damage
        self.__current_health = self.build.health

    @property
    def is_alive(self):
        return self.__current_health > 0

    def take_damage(self, damage):
        if type(damage) is not int:
            raise TypeError("Damage must be an integer")
        self.__current_health -= damage

    @property
    def state(self) -> AgentSnapshot:
        return AgentSnapshot(
            health=self.__current_health,
            damage=self.__current_damage
        )