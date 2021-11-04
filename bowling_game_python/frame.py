from dataclasses import dataclass
from enum import Enum
from typing import List

from . import errors

INITIAL_PIN_COUNT = 5
LAST_FRAME_COUNT = 10
ATTEMPTS_PER_FRAME = 3


class FrameType(str, Enum):
    open = "open"
    strike = "strike"
    spare = "spare"
    last = "last"


PIN_SCORE_MAP = {
    1: 2,
    2: 3,
    3: 5,
    4: 3,
    5: 2,
}


@dataclass
class Pins:
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

    @property
    def score(self):
        return sum(
            PIN_SCORE_MAP[idx]
            for idx, knocked_down in self.to_dict().items()
            if knocked_down
        )

    def to_dict(self):
        return {k: v for k, v in enumerate(self.__dict__.values(), start=1)}

    def __add__(self, other):
        if isinstance(other, Pins):
            return Pins.from_list(
                list(map(any, zip(*[self.__dict__.values(), other.__dict__.values()])))
            )
        raise NotImplemented


class Frame:
    def __init__(self, count):
        self._count = count
        self._knocked_down = []
        self._pins = Pins()
        self._attempts_left = ATTEMPTS_PER_FRAME

    @property
    def count(self):
        return self._count

    @property
    def score(self):
        return sum(self._knocked_down)

    @property
    def score_pins(self):
        return sum(
            PIN_SCORE_MAP[idx]
            for idx, knocked_down in self._pins.to_dict().items()
            if knocked_down
        )

    @score.setter
    def score(self, val: int):
        if not self._attempts_left:
            raise errors.NoAttemptsLeft()
        if not self.is_last_frame:
            if self.score == INITIAL_PIN_COUNT:
                raise errors.NoPinsLeft()
        self._knocked_down.append(val)
        self._attempts_left -= 1

    @property
    def attempts_left(self):
        return self._attempts_left

    @property
    def is_strike(self):
        return self.score == INITIAL_PIN_COUNT and self.attempts_left == 2

    @property
    def is_spare(self):
        return (
            self._knocked_down[0] == 0
            and self.score == INITIAL_PIN_COUNT
            and self._attempts_left == 1
        )

    @property
    def is_last_frame(self):
        return self._count == LAST_FRAME_COUNT

    @property
    def has_ended(self):
        return self.is_strike or self.is_spare

    def knock_down(self, pins: Pins = Pins()):
        self._pins = self._pins + pins

    def __eq__(self, other):
        if isinstance(other, Frame):
            return self._count == other._count
        raise NotImplemented()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._count})"

    @classmethod
    def from_previous(cls, frame: "Frame") -> "Frame":
        return Frame.create(count=frame.count + 1)

    @classmethod
    def create(cls, *, count: int = 1, type_: FrameType = FrameType.open) -> "Frame":
        if count > LAST_FRAME_COUNT:
            raise errors.GameOver

        instance = cls(count)
        if type_ == FrameType.strike:
            instance.score = INITIAL_PIN_COUNT
        if type_ == FrameType.spare:
            instance.score = 0
            instance.score = INITIAL_PIN_COUNT
        return instance
