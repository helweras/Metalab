
from metalab.battle_history import BattleHistory


class BattleHistoryFormatter:

    def format(self, history: BattleHistory) -> str:
        if not isinstance(history, BattleHistory):
            raise TypeError("history должен иметь тип BattleHistory")

        if not history.rounds:
            return "История боя пуста."

        lines = [
            "========== ИСТОРИЯ БОЯ ==========",
            f"Всего раундов: {history.total_rounds}",
            "",
        ]

        for record in history:
            lines.extend(self._format_round(record))

        lines.append("=================================")

        return "\n".join(lines)

    def _format_round(self, record) -> list[str]:
        lines = [
            f"========== РАУНД {record.round_number} ==========",
            "",
            "АГЕНТ А",
            f"  Состояние до раунда: {self._format_snapshot(record.agent_a_before)}",
            f"  Действие: {record.action_a.action_type.name}",
            f"  Цель: {record.action_a.target.name}",
            f"  Эффекты: {self._format_effects(record.effects_a)}",
            f"  Состояние после раунда: {self._format_snapshot(record.agent_a_after)}",
            "",
            "АГЕНТ Б",
            f"  Состояние до раунда: {self._format_snapshot(record.agent_b_before)}",
            f"  Действие: {record.action_b.action_type.name}",
            f"  Цель: {record.action_b.target.name}",
            f"  Эффекты: {self._format_effects(record.effects_b)}",
            f"  Состояние после раунда: {self._format_snapshot(record.agent_b_after)}",
            "",
        ]

        return lines

    @staticmethod
    def _format_snapshot(snapshot) -> str:
        return ", ".join(
            f"{attribute.name}={value}"
            for attribute, value in snapshot.attributes.items()
        )

    @staticmethod
    def _format_effects(effects) -> str:
        if not effects:
            return "Нет"

        return "; ".join(
            f"{effect.target.name}: "
            f"{effect.action_result.attribute.name} "
            f"{effect.action_result.value:+}"
            for effect in effects
        )
