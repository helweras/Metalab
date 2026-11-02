from src.metalab.build import Build


class Agent:
    def __init__(self, build: Build):
        self.build = build
        self.__current_damage = self.build.damage
        self.__current_health = self.build.health

    @property
    def damage(self):
        return self.__current_damage

    @property
    def health(self):
        return self.__current_health

    def is_alive(self):
        return self.__current_health > 0

    def take_damage(self, damage):
        if type(damage) is not int:
            raise TypeError("Damage must be an integer")
        self.__current_health -= damage
