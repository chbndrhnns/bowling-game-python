import pytest

from bowling_game_python import Frame, Ball, errors
from .conftest import one_pin, all_remaining, other_pin


class TestFrame:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_can_knock_down_pins(self, frame):
        frame.knock_down(Ball(pin_1=True))
        frame.knock_down(Ball(pin_2=True))
        assert frame._balls[0] == Ball(pin_1=True)
        assert frame._balls[1] == Ball(pin_2=True)

    def test_cannot_knock_down_same_pin_twice(self, frame):
        frame.knock_down(one_pin)
        with pytest.raises(errors.PinsDownAlready):
            frame.knock_down(one_pin)

    @pytest.mark.parametrize(
        "pins,score",
        [
            (Ball.from_list([1, 0, 0, 0, 0]), 2),
            (Ball.from_list([0, 1, 0, 0, 0]), 3),
            (Ball.from_list([0, 0, 1, 0, 0]), 5),
            (Ball.from_list([0, 0, 0, 1, 0]), 3),
            (Ball.from_list([0, 0, 0, 0, 1]), 2),
        ],
    )
    def test_can_score_single_knocked_down_pins(self, pins, score, frame):
        frame.knock_down(pins)
        assert frame.score == score

    @pytest.mark.parametrize(
        "pins,score",
        [
            (Ball.from_list([1, 0, 1, 0, 0]), 7),
        ],
    )
    def test_can_score_multiple_knocked_down_pins(self, pins, score, frame):
        frame.knock_down(pins)
        assert frame.score == score


class TestStrike:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_all_in_first_attempt_is_strike(self, frame):
        frame.knock_down(Ball.all())
        assert frame.is_strike

    def test_all_after_second_is_not_strike(self, frame):
        frame.knock_down(one_pin)
        frame.knock_down(all_remaining)
        assert not frame.is_strike

    def test_frame_ends_after_strike(self, frame):
        frame.knock_down(Ball.all())
        assert frame.is_complete


class TestSpare:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_all_in_second_attempt_is_spare(self, frame):
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.all())
        assert frame.is_spare

    def test_no_spare_if_first_not_zero(self, frame):
        frame.knock_down(one_pin)
        frame.knock_down(all_remaining)
        assert not frame.is_spare

    def test_no_spare_if_remaining_pins(self, frame):
        frame.knock_down(one_pin)
        frame.knock_down(other_pin)
        assert not frame.is_spare

    def test_frame_ends_after_spare(self, frame):
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.all())
        assert frame.is_complete


class TestLastFrame:
    @pytest.fixture
    def frame(self):
        return Frame.from_previous(Frame(9))

    def test_tenth_frame_is_created_as_special_frame(self):
        frame = Frame.from_previous(Frame(9))
        assert frame.count == 10
        assert frame.is_last_frame

    def test_cannot_create_frame_after_tenth_frame(self):
        with pytest.raises(errors.GameOver):
            Frame.from_previous(Frame(10))

    def test_three_strikes(self, frame):
        frame.knock_down(Ball.all())
        frame.knock_down(Ball.all())
        frame.knock_down(Ball.all())
        assert frame.score == 15 + 15 + 15

    def test_one_strike_one_spare(self, frame):
        frame.knock_down(Ball.all())
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.all())
        assert frame.score == 15 + 0 + 15

    def test_one_spare_one_strike(self, frame):
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.all())
        frame.knock_down(Ball.all())
        assert frame.score == 0 + 15 + 15

    def test_one_strike_two_other(self, frame):
        frame.knock_down(Ball.all())
        frame.knock_down(one_pin)
        frame.knock_down(other_pin)
        assert frame.score == 15 + 2 + 3

    def test_one_spare_one_other(self, frame):
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.all())
        frame.knock_down(other_pin)
        assert frame.score == 15 + 3

    def test_cannot_have_more_than_three_attempts(self, frame):
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.none())
        frame.knock_down(Ball.none())
        with pytest.raises(errors.NoAttemptsLeft):
            frame.knock_down(Ball.none())
