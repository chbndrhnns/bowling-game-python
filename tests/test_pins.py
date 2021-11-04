import pytest

from bowling_game_python import Pins


class TestPins:
    @pytest.fixture
    def pins(self):
        return Pins()

    def test_can_overlay_with_throw(self, pins):
        assert pins + Pins(pin_1=True) == Pins(pin_1=True)

    def test_can_score_pins(self):
        assert Pins.all().score == 15
        assert Pins.none().score == 0
