from . import errors
from .ball import Ball
from .frame import Frame


class Game:
    FRAMES_PER_GAME = 10

    def __init__(self):
        self._frames = [Frame(1)]

    @property
    def current_frame(self):
        return self._frames[-1]

    @property
    def score(self):
        return sum(frame.score for frame in self._frames)

    def throw(self, ball: Ball):
        if self._is_new_frame_needed:
            self._create_next_frame()
        self.current_frame.throw(ball)

    @property
    def _is_new_frame_needed(self):
        return not self.current_frame.balls_left and self._is_new_frame_possible

    @property
    def _is_new_frame_possible(self):
        if self.current_frame.count < self.FRAMES_PER_GAME:
            return True
        raise errors.GameOver()

    def _create_next_frame(self):
        self._frames.append(Frame.from_previous(self.current_frame))
