import pytest

from bowling_game_python.game import Game


@pytest.fixture
def game() -> Game:
    return Game()
