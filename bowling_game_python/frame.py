from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import add
from typing import List

from . import errors

INITIAL_PIN_COUNT = 5
LAST_FRAME_COUNT = 10
MAX_ATTEMPTS_PER_FRAME = 3


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


class Frame:
    def __init__(self, count):
        self._count = count
        self._attempts: List[Pins] = []

    @property
    def count(self):
        return self._count

    @property
    def score(self):
        return sum(pins.score for pins in self._attempts)

    @property
    def attempts_left(self):
        return MAX_ATTEMPTS_PER_FRAME - len(self._attempts)

    @property
    def is_strike(self):
        return len(self._attempts) == 1 and self.score == 15

    @property
    def is_spare(self):
        return (
            self._attempts[0].score == 0
            and self.score == Pins.all().score
            and self.attempts_left == 1
        )

    @property
    def is_last_frame(self):
        return self.count == LAST_FRAME_COUNT

    @property
    def is_complete(self):
        return self.is_strike or self.is_spare

    @property
    def pin_state(self):
        return reduce(add, self._attempts, Pins())

    def knock_down(self, pins: Pins):
        if not self.attempts_left:
            raise errors.NoAttemptsLeft()
        if not self.is_last_frame:
            try:
                if not self._attempts[-1].pins_left:
                    raise errors.NoPinsLeft()
            except IndexError:
                ...
            if not self.pin_state.pins_left:
                raise errors.NoPinsLeft
        self._check_pins_not_already_down(pins)
        self._attempts.append(pins)

    def _check_pins_not_already_down(self, pins: Pins):
        if not self.is_last_frame:
            already_down = [
                pin_name
                for pin_name, pin_value in pins.__dict__.items()
                if (
                    self.pin_state.__dict__.get(pin_name)
                    and pins.__dict__.get(pin_name)
                )
            ]
            if already_down:
                raise errors.PinsDownAlready(already_down=already_down)

    def __eq__(self, other):
        if isinstance(other, Frame):
            return self.count == other.count
        raise NotImplemented()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.count})"

    @classmethod
    def from_previous(cls, frame: "Frame") -> "Frame":
        return Frame.create(count=frame.count + 1)

    @classmethod
    def create(cls, *, count: int = 1, type_: FrameType = FrameType.open) -> "Frame":
        if count > LAST_FRAME_COUNT:
            raise errors.GameOver

        instance = cls(count)
        if type_ == FrameType.strike:
            instance.knock_down(Pins.all())
        if type_ == FrameType.spare:
            instance.knock_down(Pins.none())
            instance.knock_down(Pins.all())
        return instance
