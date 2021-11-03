import pytest

INITIAL_PIN_COUNT = 5

THROWS_PER_FRAME = 3


class NoThrowsLeft(Exception):
    ...


class NoPinsLeft(Exception):
    ...


class Game:
    def __init__(self):
        self._pins_left = INITIAL_PIN_COUNT
        self._throws_left = THROWS_PER_FRAME

    def throw(self, knocked_down_count: int):
        if not self._throws_left:
            raise NoThrowsLeft()
        if not self._pins_left:
            raise NoPinsLeft()
        self._throws_left -= 1
        self._pins_left -= knocked_down_count


@pytest.fixture
def game():
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
    with pytest.raises(NoThrowsLeft):
        game.throw(0)
