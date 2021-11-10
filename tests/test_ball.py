import pytest

from bowling_game_python import Ball


class TestBalls:
    @pytest.fixture
    def pins(self):
        return Ball()

    def test_can_overlay_empty_ball_with_new_ball(self, pins):
        assert pins + Ball(pin_1=True) == Ball(pin_1=True)

    def test_can_overlay_two_balls(self, pins):
        assert Ball(pin_2=True) + Ball(pin_1=True) == Ball(pin_1=True, pin_2=True)

    def test_cannot_overlay_with_already_down_pin(self):
        with pytest.raises(Exception):
            Ball(pin_1=True) + Ball(pin_1=True)

    def test_can_score_pins(self):
        assert Ball.all().score == 15
        assert Ball.none().score == 0
