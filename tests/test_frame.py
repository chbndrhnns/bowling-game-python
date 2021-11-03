import pytest

INITIAL_PIN_COUNT = 5

ATTEMPTS_PER_FRAME = 3


class NoAttemptsLeft(Exception):
    ...


class NoPinsLeft(Exception):
    ...


class Frame:
    def __init__(self, count):
        self._count = count
        self._knocked_down = 0
        self._attempts_left = ATTEMPTS_PER_FRAME

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

    def __eq__(self, other):
        if isinstance(other, Frame):
            return self._count == other._count
        raise NotImplemented()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._count})"


class Game:
    def __init__(self):
        self._pins_left = INITIAL_PIN_COUNT
        self._attempts_left = ATTEMPTS_PER_FRAME
        self._current_frame = 1
        self._frames = [Frame(1)]

    @property
    def frame(self):
        return self._frames[self._current_frame - 1]

    @property
    def score(self):
        return sum(frame.score for frame in self._frames)

    def throw(self, knocked_down_count: int):
        self.frame.score = knocked_down_count
        if not self.frame.attempts_left:
            frame = Frame(self._current_frame + 1)
            self._frames.append(frame)
            self._current_frame = frame._count


@pytest.fixture
def game() -> Game:
    return Game()


def test_can_frame_a_ball(game):
    game.throw(0)


def test_cannot_throw_if_no_pins_left(game):
    game.throw(5)
    with pytest.raises(NoPinsLeft):
        game.throw(0)


class TestFrame:
    def test_game_has_a_frame(self, game):
        assert game.frame == Frame(1)

    def test_second_frame_after_three_attempts(self, game):
        game.throw(1)
        game.throw(1)
        game.throw(1)
        assert game.frame == Frame(2)


class TestScore:
    def test_game_counts_score_for_one_throw(self, game):
        game.throw(1)
        assert game.score == 1

    def test_game_counts_score_for_two_throws(self, game):
        game.throw(1)
        game.throw(1)
        assert game.score == 2
