import abc


class classproperty:
    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, owner):
        return self._fn(owner)


class Pin(abc.ABC):
    __score__ = None

    @classproperty
    def score(self):
        return self.__score__


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
