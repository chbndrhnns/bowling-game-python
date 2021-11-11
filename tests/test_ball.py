import pytest

from bowling_game_python import Ball, pins, errors


class TestBalls:
    @pytest.fixture
    def ball(self):
        return Ball()

    def test_from_list(self):
        assert Ball.from_list([1, 0, 0, 0, 0]).pins_down == [pins.CornerLeft]

    def test_from_constructor(self):
        ball = Ball([pins.CornerLeft])
        assert ball.pins_down == [pins.CornerLeft]

    def test_can_overlay_empty_ball_with_new_ball(self, ball):
        actual = ball + Ball([pins.CornerLeft])
        assert actual.pins_left == Ball([pins.CornerLeft]).pins_left

    def test_can_overlay_two_balls(self, ball):
        assert Ball([pins.TwoPinLeft]) + Ball([pins.CornerLeft]) == Ball(
            [pins.CornerLeft, pins.TwoPinLeft]
        )

    def test_cannot_overlay_with_already_down_pin(self):
        with pytest.raises(errors.PinsDownAlready):
            Ball([pins.CornerLeft]) + Ball([pins.CornerLeft])

    def test_can_score_ball(self):
        assert Ball.all().score == 15
        assert Ball.none().score == 0
