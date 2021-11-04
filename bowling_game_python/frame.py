from enum import Enum

from bowling_game_python.errors import NoAttemptsLeft, NoPinsLeft

INITIAL_PIN_COUNT = 5
ATTEMPTS_PER_FRAME = 3


class FrameType(str, Enum):
    regular = "regular"
    strike = "strike"


class Frame:
    def __init__(self, count):
        self._count = count
        self._knocked_down = 0
        self._attempts_left = ATTEMPTS_PER_FRAME

    @property
    def count(self):
        return self._count

    @property
    def score(self):
        return self._knocked_down

    @score.setter
    def score(self, val: int):
        if not self._attempts_left:
            raise NoAttemptsLeft()
        if self._knocked_down == INITIAL_PIN_COUNT:
            raise NoPinsLeft()
        self._knocked_down += val
        self._attempts_left -= 1

    @property
    def attempts_left(self):
        return self._attempts_left

    @property
    def is_strike(self):
        return self._knocked_down == INITIAL_PIN_COUNT and self.attempts_left == 2

    @property
    def has_ended(self):
        return self.is_strike

    def __eq__(self, other):
        if isinstance(other, Frame):
            return self._count == other._count
        raise NotImplemented()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._count})"

    @classmethod
    def from_previous(cls, frame: "Frame") -> "Frame":
        return cls(frame.count + 1)

    @classmethod
    def create(cls, *, count: int = 1, type_: FrameType = FrameType.regular) -> "Frame":
        instance = cls(count)
        if type_ == FrameType.strike:
            instance.score = INITIAL_PIN_COUNT
        return instance
