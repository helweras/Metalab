
from dataclasses import dataclass

from metalab.round_record import RoundRecord


@dataclass(frozen=True)
class BattleHistory:
    rounds: tuple[RoundRecord, ...] = ()

    def __post_init__(self) -> None:
        rounds = tuple(self.rounds)
        object.__setattr__(self, "rounds", rounds)

        for index, record in enumerate(rounds, start=1):
            if not isinstance(record, RoundRecord):
                raise TypeError(
                    "Every history entry must be a RoundRecord"
                )

            if record.round_number != index:
                raise ValueError(
                    "Round numbers must be sequential and start at 1"
                )

    @property
    def total_rounds(self) -> int:
        return len(self.rounds)

    def get_round(self, round_number: int) -> RoundRecord:
        if not isinstance(round_number, int) or isinstance(round_number, bool):
            raise TypeError("round_number must be an integer")

        if round_number < 1 or round_number > self.total_rounds:
            raise IndexError("Round number is out of range")

        return self.rounds[round_number - 1]

    def __len__(self) -> int:
        return self.total_rounds

    def __iter__(self):
        return iter(self.rounds)
