import pytest

from bowling_game_python import Frame, errors


def test_cannot_throw_if_no_pins_left(game):
    game.throw(5)
    with pytest.raises(errors.NoPinsLeft):
        game.throw(0)


def test_can_throw_a_ball(game):
    game.throw(0)


class TestFrame:
    def test_game_has_a_frame(self, game):
        assert game.current_frame == Frame(1)

    def test_second_frame_after_three_attempts(self, game):
        game.throw(1)
        game.throw(1)
        game.throw(1)
        assert game.current_frame == Frame(2)


class TestScore:
    def test_game_counts_score_for_one_throw(self, game):
        game.throw(1)
        assert game.score == 1

    def test_game_counts_score_for_two_throws(self, game):
        game.throw(1)
        game.throw(1)
        assert game.score == 2
