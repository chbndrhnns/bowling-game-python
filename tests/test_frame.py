import pytest

INITIAL_PIN_COUNT = 5

ATTEMPTS_PER_FRAME = 3


class NoAttemptsLeft(Exception):
    ...


class NoPinsLeft(Exception):
    ...


class Game:
    def __init__(self):
        self._pins_left = INITIAL_PIN_COUNT
        self._attempts_left = ATTEMPTS_PER_FRAME
        self._frames = []

    @property
    def frame(self):
        if self._attempts_left == 0:
            return 2
        return 1

    @property
    def score(self):
        return INITIAL_PIN_COUNT - self._pins_left

    def throw(self, knocked_down_count: int):
        if not self._attempts_left:
            raise NoAttemptsLeft()
        if not self._pins_left:
            raise NoPinsLeft()
        self._attempts_left -= 1
        self._pins_left -= knocked_down_count


@pytest.fixture
def game() -> Game:
    return Game()


def test_can_frame_a_ball(game):
    game.throw(0)


def test_cannot_throw_if_no_pins_left(game):
    game.throw(5)
    with pytest.raises(NoPinsLeft):
        game.throw(0)


def test_cannot_throw_if_throws_used_up(game):
    game.throw(0)
    game.throw(0)
    game.throw(0)
    with pytest.raises(NoAttemptsLeft):
        game.throw(0)


class TestFrame:
    def test_game_has_a_frame(self, game):
        assert game.frame == 1

    def test_second_frame_after_three_attempts(self, game):
        game.throw(1)
        game.throw(1)
        game.throw(1)
        assert game.frame == 2


class TestScore:
    def test_game_counts_score_for_one_throw(self, game):
        game.throw(1)
        assert game.score == 1

    def test_game_counts_score_for_two_throws(self, game):
        game.throw(1)
        game.throw(1)
        assert game.score == 2
