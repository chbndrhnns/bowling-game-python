from . import errors
from .frame import Frame

MAX_FRAME_COUNT = 10


class Game:
    def __init__(self):
        self._frames = [Frame(1)]

    @property
    def current_frame(self):
        return self._frames[-1]

    @property
    def score(self):
        return sum(frame.score for frame in self._frames)

    def throw(self, knocked_down_count: int):
        self.current_frame.score = knocked_down_count
        if not self.current_frame.attempts_left:
            self._add_frame()

    def _add_frame(self):
        if self.current_frame.count == MAX_FRAME_COUNT:
            raise errors.GameOver()
        self._frames.append(Frame.from_previous(self.current_frame))
