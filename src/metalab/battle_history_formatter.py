from metalab.agent_snapshot import AgentSnapshot
from metalab.battle_history import BattleHistory
from metalab.effect import Effect
from metalab.round_record import RoundRecord


class BattleHistoryFormatter:
    """Форматирует историю боя в текстовый вид."""

    def format(self, history: BattleHistory) -> str:
        """Форматирует всю историю боя."""
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

    def _format_round(self, record: RoundRecord) -> list[str]:
        """Форматирует запись одного раунда."""
        if not isinstance(record, RoundRecord):
            raise TypeError("record должен иметь тип RoundRecord")

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
    def _format_snapshot(snapshot: AgentSnapshot) -> str:
        """Форматирует снимок состояния агента."""
        if not isinstance(snapshot, AgentSnapshot):
            raise TypeError("snapshot должен иметь тип AgentSnapshot")

        return ", ".join(
            f"{attribute.name}={value}"
            for attribute, value in snapshot.attributes.items()
        )

    @staticmethod
    def _format_effects(effects: tuple[Effect, ...]) -> str:
        """Форматирует список эффектов."""
        if not isinstance(effects, tuple):
            raise TypeError("effects должен быть кортежем")

        if not all(isinstance(effect, Effect) for effect in effects):
            raise TypeError("Все элементы effects должны иметь тип Effect")

        if not effects:
            return "Нет"

        return "; ".join(
            f"{effect.target.name}: "
            f"{effect.action_result.attribute.name} "
            f"{effect.action_result.value:+}"
            for effect in effects
        )
