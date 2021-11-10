from dataclasses import dataclass
from typing import List

from bowling_game_python import errors, pins

PIN_COUNT = 5
PIN_SCORE_MAP = {
    1: 2,
    2: 3,
    3: 5,
    4: 3,
    5: 2,
}


@dataclass
class Ball:
    pin_1: bool = False
    pin_2: bool = False
    pin_3: bool = False
    pin_4: bool = False
    pin_5: bool = False

    # pin_1_cls: pins.CornerLeft = pins.CornerLeft()

    @classmethod
    def from_list(cls, data: List):
        if len(data) != PIN_COUNT:
            raise ValueError("Need 5 values")
        return cls(*data)

    @classmethod
    def all(cls):
        return Ball.from_list(
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
        return Ball()

    @property
    def score(self):
        return sum(
            PIN_SCORE_MAP[idx]
            for idx, knocked_down in {
                k: v for k, v in enumerate(self.dict().values(), start=1)
            }.items()
            if knocked_down
        )

    @property
    def pins_left(self):
        return len(list((pin for pin in self.dict().values() if not pin)))

    def dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.endswith("_cls")}

    def __add__(self, other):
        if isinstance(other, Ball):
            if already_down := [
                pin
                for pin in other.dict().keys()
                if other.dict().get(pin) and self.dict().get(pin)
            ]:
                raise errors.PinsDownAlready(already_down=already_down)
            return Ball.from_list(
                list(map(any, zip(*[self.dict().values(), other.dict().values()])))
            )
        raise NotImplemented
