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


def test_pin_is_equal_if_is_down_is_equal():
    assert pins.TwoPinLeft() == pins.TwoPinLeft()
    assert pins.TwoPinLeft(down=True) == pins.TwoPinLeft(down=True)
    assert pins.Head(down=True) != pins.TwoPinLeft(down=True)


def test_pin_down():
    pin = pins.CornerLeft()
    assert not pin.is_down
    pin.knock_down()
    assert pin.is_down
