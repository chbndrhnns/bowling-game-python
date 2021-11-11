from functools import reduce
from operator import add
from typing import List

from . import errors
from .ball import Ball

LAST_FRAME_COUNT = 10
MAX_ATTEMPTS_PER_FRAME = 3


class Frame:
    def __init__(self, count):
        self._count: int = count
        self._balls: List[Ball] = []

    @property
    def count(self) -> int:
        return self._count

    @property
    def score(self) -> int:
        return sum(ball.score for ball in self._balls)

    @property
    def current_ball(self) -> Ball:
        return self._balls[-1]

    @property
    def balls_left(self) -> int:
        return MAX_ATTEMPTS_PER_FRAME - len(self._balls)

    @property
    def is_strike(self):
        return self.balls_left == 2 and self.current_ball.score == Ball.MAX_SCORE

    @property
    def is_spare(self):
        return (
            self.balls_left == 1
            and self.get_ball(1).score == 0
            and self.current_ball.score == Ball.MAX_SCORE
        )

    @property
    def is_last_frame(self):
        return self.count == LAST_FRAME_COUNT

    @property
    def is_complete(self):
        return self.is_strike or self.is_spare or not self.balls_left

    @property
    def pin_state(self):
        return reduce(add, self._balls, Ball())

    def get_ball(self, count: int):
        return self._balls[count - 1]

    def throw(self, ball: Ball):
        if self._can_throw():
            self._add_ball(ball)

    def _can_throw(self):
        if self.is_complete or not self.balls_left:
            raise errors.NoBallsLeft()
        if not self.pin_state.pins_left:
            raise errors.NoPinsLeft()
        return True

    def _add_ball(self, ball: Ball):
        self._validate_ball(ball)
        self._balls.append(ball)

    def _validate_ball(self, ball: Ball):
        if self._balls:
            self._balls[-1] + ball

    def __eq__(self, other):
        if isinstance(other, Frame):
            return self.count == other.count
        raise NotImplementedError()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.count})"

    @classmethod
    def from_previous(cls, frame: "Frame") -> "Frame":
        if frame.is_last_frame:
            raise errors.GameOver

        next_frame_count = frame.count + 1
        if next_frame_count == LAST_FRAME_COUNT:
            return LastFrame()

        return cls(count=next_frame_count)


class LastFrame(Frame):
    def __init__(self):
        super().__init__(count=LAST_FRAME_COUNT)

    def _can_throw(self):
        if not self.balls_left:
            raise errors.NoBallsLeft()
        return True

    def _validate_ball(self, ball: Ball):
        return True
