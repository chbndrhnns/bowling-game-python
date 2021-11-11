from typing import List, Type

from bowling_game_python import errors, pins


class Ball:
    __pin_setup__ = [
        pins.CornerLeft,
        pins.TwoPinLeft,
        pins.Head,
        pins.TwoPinRight,
        pins.CornerRight,
    ]

    def __init__(self, down: List[Type[pins.Pin]] = None):
        self._pins: List[pins.Pin] = [pin() for pin in self.__pin_setup__]

        down = down or []
        if len(down) == len(self.__pin_setup__):
            self._pins = [pin.knock_down() for pin in self._pins]

        elif len(down) < len(self.__pin_setup__):
            for pin in down:
                self._pins[pin.position - 1] = pin(down=True)

    def get_pin_by_position(self, position: int):
        return self._pins[position - 1]

    def get_pin(self, pin_type: Type[pins.Pin]):
        return [pin for pin in self._pins if isinstance(pin, pin_type)][0]

    @classmethod
    def from_list(cls, data: List[int]):
        if len(data) != len(cls.__pin_setup__):
            raise ValueError("Need 5 values")
        return cls([pin for idx, pin in enumerate(cls.__pin_setup__) if data[idx]])

    @classmethod
    def all(cls):
        return cls([pin for pin in cls.__pin_setup__])

    @classmethod
    def none(cls):
        return cls()

    @property
    def score(self):
        return sum(pin.score for pin in self._pins if pin.is_down)

    @property
    def pins_left(self):
        return [pin.__class__ for pin in self._pins if not pin.is_down]

    @property
    def pins(self):
        return self._pins

    @property
    def pins_down(self):
        return [pin.__class__ for pin in self._pins if pin.is_down]

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        self_down = set(self.pins_down)
        other_down = set(other.pins_down)

        if duplicates := self_down & other_down:
            raise errors.PinsDownAlready(already_down=duplicates)
        return self.__class__(list(self_down | other_down))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self._pins == other.pins

    def __repr__(self):
        return f"{self.__class__.__name__}({[pin.position for pin in self.pins if pin.is_down]})"
