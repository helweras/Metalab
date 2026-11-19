from metalab.agent_state import AgentState
from metalab.action import Action, ActionType
from metalab.target import Target


class AgentStrategy:

    def __init__(self, available_actions: tuple[ActionType, ...]) -> None:
        self.__available_actions = available_actions

    def choose_action(self, state: AgentState) -> Action:
        action_type = self.__available_actions[0]
        if action_type == ActionType.ATTACK:
            target = Target.ENEMY
        else:
            raise ValueError(f"Unsupported action type: {action_type}")

        return Action(
            action_type=action_type,
            target=target,
        )
