from metalab.agent_state import AgentState
from metalab.action import Action, ActionType
from metalab.target import Target


class AgentStrategy:

    def choose_action(self, state: AgentState) -> Action:
        return Action(
            action_type=ActionType.ATTACK,
            target=Target.ENEMY,
        )
