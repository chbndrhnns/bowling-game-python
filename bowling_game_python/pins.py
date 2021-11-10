import abc


class classproperty:
    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, owner):
        return self._fn(owner)


class Pin(abc.ABC):
    __score__ = None

    def __init__(self):
        self._is_down = False

    @classproperty
    def score(self):
        return self.__score__

    @property
    def is_down(self):
        return self._is_down

    def knock_down(self):
        self._is_down = True


class CornerLeft(Pin):
    __score__ = 2


class TwoPinLeft(Pin):
    __score__ = 3


class Head(Pin):
    __score__ = 5


class CornerRight(Pin):
    __score__ = 2


class TwoPinRight(Pin):
    __score__ = 3
