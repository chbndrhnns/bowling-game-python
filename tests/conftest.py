import pytest

from bowling_game_python import Ball
from bowling_game_python.game import Game


@pytest.fixture
def game() -> Game:
    return Game()


one_pin = Ball.from_list([1, 0, 0, 0, 0])
all_remaining = Ball.from_list(
    [
        0,
        1,
        1,
        1,
        1,
    ]
)
other_pin = Ball.from_list([0, 1, 0, 0, 0])
