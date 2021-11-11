import pytest

from bowling_game_python import Frame, errors, Ball
from .conftest import one_pin, other_pin


def test_cannot_throw_if_no_pins_left(game):
    game.throw(Ball.all_down())
    with pytest.raises(errors.NoBallsLeft):
        game.throw(one_pin)


def test_can_throw_a_ball(game):
    game.throw(one_pin)


def test_game_has_a_frame(game):
    assert game.current_frame == Frame(1)


def test_second_frame_after_three_attempts(game):
    # Frame 1
    game.throw(Ball.from_list([1, 0, 0, 0, 0]))
    game.throw(Ball.from_list([0, 1, 0, 0, 0]))
    game.throw(Ball.from_list([0, 0, 1, 0, 0]))
    # Frame 2
    game.throw(Ball.from_list([0, 0, 0, 1, 0]))
    assert game.current_frame == Frame(2)


def test_game_ends_after_ten_frames(game):
    [game._create_next_frame() for _ in range(9)]
    game.throw(Ball())
    game.throw(one_pin)
    game.throw(other_pin)
    with pytest.raises(errors.GameOver):
        game.throw(one_pin)


class TestScore:
    def test_game_counts_score_for_one_throw(self, game):
        game.throw(one_pin)
        assert game.score == 2

    def test_game_counts_score_for_two_throws(self, game):
        game.throw(one_pin)
        game.throw(other_pin)
        assert game.score == 5
