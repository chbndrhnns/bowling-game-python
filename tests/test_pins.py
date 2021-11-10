import pytest

from bowling_game_python import pins


@pytest.mark.parametrize(
    "pin, score",
    [
        (pins.CornerLeft, 2),
        (pins.TwoPinLeft, 3),
        (pins.Head, 5),
        (pins.TwoPinRight, 3),
        (pins.CornerRight, 2),
    ],
)
class TestPins:
    def test_create_pins(self, pin, score):
        assert pin()

    def test_pin_score(self, pin, score):
        assert pin.score == score
