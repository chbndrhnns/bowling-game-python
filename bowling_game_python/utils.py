class classproperty:
    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, owner):
        return self._fn(owner)
