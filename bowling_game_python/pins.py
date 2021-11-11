import abc


class classproperty:
    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, owner):
        return self._fn(owner)


class Pin(abc.ABC):
    __score__ = None
    __position__ = None

    def __init__(self, *, down: bool = False):
        self._is_down = down

    @classproperty
    def score(self):
        return self.__score__

    @classproperty
    def position(self):
        return self.__position__

    @property
    def is_down(self):
        return self._is_down

    def knock_down(self):
        self._is_down = True
        return self

    def __eq__(self, other):
        if not isinstance(other, Pin):
            raise NotImplementedError()
        if not isinstance(other, self.__class__):
            return False

        return self.is_down == other.is_down


class CornerLeft(Pin):
    __position__ = 1
    __score__ = 2


class TwoPinLeft(Pin):
    __position__ = 2
    __score__ = 3


class Head(Pin):
    __position__ = 3
    __score__ = 5


class CornerRight(Pin):
    __position__ = 4
    __score__ = 2


class TwoPinRight(Pin):
    __position__ = 5
    __score__ = 3
