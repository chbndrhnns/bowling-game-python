import pytest

from bowling_game_python import Ball


class TestBalls:
    @pytest.fixture
    def pins(self):
        return Ball()

    def test_can_overlay_with_throw(self, pins):
        assert pins + Ball(pin_1=True) == Ball(pin_1=True)

    def test_can_score_pins(self):
        assert Ball.all().score == 15
        assert Ball.none().score == 0
