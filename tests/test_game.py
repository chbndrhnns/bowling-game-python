import pytest

from bowling_game_python import Frame, errors, FrameType


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

    def test_game_ends_after_ten_frames(self, game):
        [game._reset() for _ in range(9)]
        game.throw(1)
        game.throw(1)
        with pytest.raises(errors.GameOver):
            game.throw(1)


class TestScore:
    def test_game_counts_score_for_one_throw(self, game):
        game.throw(1)
        assert game.score == 1

    def test_game_counts_score_for_two_throws(self, game):
        game.throw(1)
        game.throw(1)
        assert game.score == 2


class TestStrike:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_can_create_strike_frame(self):
        assert Frame.create(type_=FrameType.strike)

    def test_all_in_first_attempt_is_strike(self, frame):
        frame.score = 5
        assert frame.is_strike

    def test_all_after_second_is_not_strike(self, frame):
        frame.score = 2
        frame.score = 3
        assert not frame.is_strike

    def test_frame_ends_after_strike(self, frame):
        frame.score = 5
        assert frame.has_ended


class TestSpare:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_can_create_spare_frame(self):
        frame = Frame.create(type_=FrameType.spare)
        assert frame.is_spare

    def test_all_in_second_attempt_is_spare(self, frame):
        frame.score = 0
        frame.score = 5
        assert frame.is_spare

    def test_no_spare_if_first_not_zero(self, frame):
        frame.score = 1
        frame.score = 4
        assert not frame.is_spare

    def test_no_spare_if_remaining_pins(self, frame):
        frame.score = 1
        frame.score = 2
        assert not frame.is_spare

    def test_frame_ends_after_spare(self, frame):
        frame.score = 0
        frame.score = 5
        assert frame.has_ended


class TestLastFrame:
    @pytest.fixture
    def frame(self):
        return Frame(10)

    def test_tenth_frame_is_created_as_special_frame(self):
        frame = Frame.from_previous(Frame(9))
        assert frame.count == 10
        assert frame.is_last_frame

    def test_cannot_create_frame_after_tenth_frame(self):
        with pytest.raises(errors.GameOver):
            Frame.from_previous(Frame(10))

    def test_three_strikes(self, frame):
        frame.score = 5
        frame.score = 5
        frame.score = 5
        assert frame.score == 15

    def test_one_strike_two_spares(self, frame):
        frame.score = 5
        frame.score = 0
        frame.score = 5
        assert frame.score == 10

    def test_one_spare_one_strike(self, frame):
        frame.score = 0
        frame.score = 5
        frame.score = 5
        assert frame.score == 10

    def test_one_strike_two_other(self, frame):
        frame.score = 5
        frame.score = 3
        frame.score = 3
        assert frame.score == 11

    def test_one_spare_one_other(self, frame):
        frame.score = 0
        frame.score = 5
        frame.score = 2
        assert frame.score == 7

    def test_cannot_have_more_than_three_attempts(self, frame):
        frame.score = 1
        frame.score = 1
        frame.score = 1
        with pytest.raises(errors.NoAttemptsLeft):
            frame.score = 1
