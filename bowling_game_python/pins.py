from dataclasses import dataclass
from typing import List

INITIAL_PIN_COUNT = 5
PIN_SCORE_MAP = {
    1: 2,
    2: 3,
    3: 5,
    4: 3,
    5: 2,
}


@dataclass
class Pins:
    # REFACTOR: Move to own module
    pin_1: bool = False
    pin_2: bool = False
    pin_3: bool = False
    pin_4: bool = False
    pin_5: bool = False

    @classmethod
    def from_list(cls, data: List):
        if len(data) != INITIAL_PIN_COUNT:
            raise ValueError("Need 5 values")
        return cls(*data)

    @classmethod
    def all(cls):
        return Pins.from_list(
            [
                1,
                1,
                1,
                1,
                1,
            ]
        )

    @classmethod
    def none(cls):
        return Pins()

    @property
    def score(self):
        return sum(
            PIN_SCORE_MAP[idx]
            for idx, knocked_down in self.to_dict().items()
            if knocked_down
        )

    @property
    def pins_left(self):
        return len(list((pin for pin in self.__dict__.values() if not pin)))

    def to_dict(self):
        return {k: v for k, v in enumerate(self.__dict__.values(), start=1)}

    def __add__(self, other):
        if isinstance(other, Pins):
            return Pins.from_list(
                list(map(any, zip(*[self.__dict__.values(), other.__dict__.values()])))
            )
        raise NotImplemented
