from metalab.action import Action
from metalab.effect import Effect, EffectTarget
from metalab.action_rules import AttackRules


class Attack(Action):
    def return_effect(self) -> Effect:
        return Effect(
            action_rule=AttackRules(),
            target=EffectTarget.ENEMY
        )


