from enum import Enum
from functools import reduce
from operator import add
from typing import List

from . import errors
from .pins import Pins

LAST_FRAME_COUNT = 10
MAX_ATTEMPTS_PER_FRAME = 3


class FrameType(str, Enum):
    open = "open"
    strike = "strike"
    spare = "spare"
    last = "last"


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
