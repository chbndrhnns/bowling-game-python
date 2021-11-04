import pytest

from bowling_game_python import Frame, errors, FrameType, Pins

one_pin = Pins.from_list([1, 0, 0, 0, 0])
other_pin = Pins.from_list([0, 1, 0, 0, 0])


def test_cannot_throw_if_no_pins_left(game):
    game.throw(Pins.all())
    with pytest.raises(errors.NoPinsLeft):
        game.throw(one_pin)


def test_can_throw_a_ball(game):
    game.throw(one_pin)


class TestPins:
    @pytest.fixture
    def pins(self):
        return Pins()

    def test_can_overlay_with_throw(self, pins):
        assert pins + Pins(pin_1=True) == Pins(pin_1=True)

    def test_can_score_pins(self):
        assert Pins.all().score == 15
        assert Pins.none().score == 0


class TestGame:
    def test_game_has_a_frame(self, game):
        assert game.current_frame == Frame(1)

    def test_second_frame_after_three_attempts(self, game):
        game.throw(one_pin)
        game.throw(one_pin)
        game.throw(one_pin)
        assert game.current_frame == Frame(2)

    def test_game_ends_after_ten_frames(self, game):
        [game._reset() for _ in range(9)]
        game.throw(one_pin)
        game.throw(one_pin)
        with pytest.raises(errors.GameOver):
            game.throw(one_pin)


class TestFrame:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_can_knock_down_pins(self, frame):
        frame.knock_down(Pins(pin_1=True))
        assert frame._attempts[0] == Pins(pin_1=True)

    @pytest.mark.parametrize(
        "pins,score",
        [
            (Pins.from_list([1, 0, 0, 0, 0]), 2),
            (Pins.from_list([0, 1, 0, 0, 0]), 3),
            (Pins.from_list([0, 0, 1, 0, 0]), 5),
            (Pins.from_list([0, 0, 0, 1, 0]), 3),
            (Pins.from_list([0, 0, 0, 0, 1]), 2),
        ],
    )
    def test_can_score_single_knocked_down_pins(self, pins, score, frame):
        frame.knock_down(pins)
        assert frame.score == score

    @pytest.mark.parametrize(
        "pins,score",
        [
            (Pins.from_list([1, 0, 1, 0, 0]), 7),
        ],
    )
    def test_can_score_multiple_knocked_down_pins(self, pins, score, frame):
        frame.knock_down(pins)
        assert frame.score == score


class TestScore:
    def test_game_counts_score_for_one_throw(self, game):
        game.throw(one_pin)
        assert game.score == 2

    def test_game_counts_score_for_two_throws(self, game):
        game.throw(one_pin)
        game.throw(other_pin)
        assert game.score == 5


class TestStrike:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_can_create_strike_frame(self):
        assert Frame.create(type_=FrameType.strike)

    def test_all_in_first_attempt_is_strike(self, frame):
        frame.knock_down(Pins.all())
        assert frame.is_strike

    def test_all_after_second_is_not_strike(self, frame):
        frame.knock_down(one_pin)
        frame.knock_down(Pins.all())
        assert not frame.is_strike

    def test_frame_ends_after_strike(self, frame):
        frame.knock_down(Pins.all())
        assert frame.is_complete


class TestSpare:
    @pytest.fixture
    def frame(self):
        return Frame(1)

    def test_can_create_spare_frame(self):
        frame = Frame.create(type_=FrameType.spare)
        assert frame.is_spare

    def test_all_in_second_attempt_is_spare(self, frame):
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.all())
        assert frame.is_spare

    def test_no_spare_if_first_not_zero(self, frame):
        frame.knock_down(one_pin)
        frame.knock_down(Pins.all())
        assert not frame.is_spare

    def test_no_spare_if_remaining_pins(self, frame):
        frame.knock_down(one_pin)
        frame.knock_down(other_pin)
        assert not frame.is_spare

    def test_frame_ends_after_spare(self, frame):
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.all())
        assert frame.is_complete


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
        frame.knock_down(Pins.all())
        frame.knock_down(Pins.all())
        frame.knock_down(Pins.all())
        assert frame.score == 45

    @pytest.mark.skip
    def test_one_strike_one_spare(self, frame):
        frame.knock_down(Pins.all())
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.all())
        assert frame.score == 30

    @pytest.mark.skip
    def test_one_spare_one_strike(self, frame):
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.all())
        frame.knock_down(Pins.all())
        assert frame.score == 10

    @pytest.mark.skip
    def test_one_strike_two_other(self, frame):
        frame.knock_down(Pins.all())
        frame.score = 3
        frame.score = 3
        assert frame.score == 11

    @pytest.mark.skip
    def test_one_spare_one_other(self, frame):
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.all())
        frame.score = 2
        assert frame.score == 7

    def test_cannot_have_more_than_three_attempts(self, frame):
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.none())
        frame.knock_down(Pins.none())
        with pytest.raises(errors.NoAttemptsLeft):
            frame.knock_down(Pins.none())
