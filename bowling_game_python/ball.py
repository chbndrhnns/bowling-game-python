from typing import Type, Set

from . import errors, pins
from .utils import classproperty


class Ball:
    __pin_setup__ = [
        pins.CornerLeft,
        pins.TwoPinLeft,
        pins.Head,
        pins.TwoPinRight,
        pins.CornerRight,
    ]
    MAX_SCORE = 15

    def __init__(self, pins_down: list[Type[pins.Pin]] = None):
        self._pins: list[pins.Pin] = self._initialize_pins()

        for pin in pins_down or []:
            self.knock_down(pin)

    def knock_down(self, pin: pins.Pin):
        self.get_pin(pin).knock_down()

    def get_pin_by_position(self, position: int):
        return self._pins[position - 1]

    def get_pin(self, pin_type: Type[pins.Pin]):
        return [pin for pin in self._pins if isinstance(pin, pin_type)][0]

    def _initialize_pins(self):
        return [pin() for pin in self.__pin_setup__]

    @classproperty
    def pin_count(cls) -> int:
        return len(cls.__pin_setup__)

    @property
    def score(self):
        return sum(pin.score for pin in self.pins_down)

    @property
    def pins_down(self) -> Set:
        return {pin.__class__ for pin in self._pins if pin.is_down}

    @property
    def pins_left(self) -> Set:
        return {pin.__class__ for pin in self._pins if not pin.is_down}

    @property
    def pins(self):
        return self._pins

    @classmethod
    def from_list(cls, data: list[int]):
        if len(data) != cls.pin_count:
            raise ValueError(f"Need {len(cls.__pin_setup__)} values")
        return cls([pin for idx, pin in enumerate(cls.__pin_setup__) if data[idx]])

    @classmethod
    def all_down(cls):
        return cls([pin for pin in cls.__pin_setup__])

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        if duplicates := self.pins_down & other.pins_down:
            raise errors.PinsDownAlready(already_down=duplicates)
        return self.__class__(list(self.pins_down | other.pins_down))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self._pins == other.pins

    def __repr__(self):
        return f"{self.__class__.__name__}({[pin.position for pin in self.pins if pin.is_down]})"
