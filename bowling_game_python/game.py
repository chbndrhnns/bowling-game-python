from . import errors
from .pins import Pins
from .frame import Frame

FRAMES_PER_GAME = 10


class Game:
    def __init__(self):
        self._frames = [Frame(1)]

    @property
    def current_frame(self):
        return self._frames[-1]

    @property
    def score(self):
        return sum(frame.score for frame in self._frames)

    def throw(self, pins: Pins):
        if self._is_new_frame_needed:
            self._create_next_frame()
        self.current_frame.knock_down(pins)

    @property
    def _is_new_frame_needed(self):
        return not self.current_frame.attempts_left and self._is_new_frame_possible

    @property
    def _is_new_frame_possible(self):
        if self.current_frame.count < FRAMES_PER_GAME:
            return True
        raise errors.GameOver()

    def _create_next_frame(self):
        self._frames.append(Frame.from_previous(self.current_frame))
