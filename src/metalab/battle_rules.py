from metalab.battle_outcome import BattleOutcome
from metalab.battle_settings import BattleSettings


class BattleRules:
    def __init__(self, settings: BattleSettings):
        if not isinstance(settings, BattleSettings):
            raise TypeError("settings must be a BattleSettings")

        self.__settings = settings

    def determine_outcome(
        self,
        agent_a_alive: bool,
        agent_b_alive: bool,
        current_round: int,
    ) -> BattleOutcome | None:

        if type(agent_a_alive) is not bool:
            raise TypeError("agent_a_alive must be a bool")

        if type(agent_b_alive) is not bool:
            raise TypeError("agent_b_alive must be a bool")

        if type(current_round) is not int:
            raise TypeError("current_round must be an integer")

        if current_round < 0:
            raise ValueError("current_round must be positive")

        if not agent_a_alive and not agent_b_alive:
            return BattleOutcome.BOTH_LOST

        if not agent_a_alive:
            return BattleOutcome.B_WON

        if not agent_b_alive:
            return BattleOutcome.A_WON

        if current_round >= self.__settings.max_rounds:
            return BattleOutcome.BOTH_WON

        return None
