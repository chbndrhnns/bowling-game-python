from bowling_game_python.frame import Frame


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
            self._frames.append(Frame.from_previous(self.current_frame))
