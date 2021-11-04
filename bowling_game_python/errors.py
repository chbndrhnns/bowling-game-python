class NoAttemptsLeft(Exception):
    ...


class NoPinsLeft(Exception):
    ...


class GameOver(Exception):
    ...


class PinsDownAlready(Exception):
    def __init__(self, message=None, already_down=None):
        self._message = message
        self._already_down = already_down
